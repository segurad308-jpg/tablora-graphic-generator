import os
import pandas as pd 
def load_data(file) -> pd.DataFrame:
    def detect_decimal(file, sample_size=5000):
        """Guess whether the CSV uses ',' or '.' as the decimal separator by inspecting a sample."""
        sample = file.read(sample_size).decode("utf-8", errors="ignore")
        file.seek(0)  # We consumed the file while reading: reset the cursor to the start before pandas re-reads it.

        comma_decimal = sample.count(",") and any(
            c.isdigit() and n == "," and p.isdigit()
            for p, n, c in zip(sample, sample[1:], sample[2:])
        )

        dot_decimal = sample.count(".") and any(
            c.isdigit() and n == "." and p.isdigit()
            for p, n, c in zip(sample, sample[1:], sample[2:])
        )

        if comma_decimal and not dot_decimal:
            return ","
        if dot_decimal and not comma_decimal:
            return "."

        return "."

    try:
        extension = os.path.splitext(file.name)[1].lower()

        if extension == ".csv":
            decimal = detect_decimal(file)
            df = pd.read_csv(
                file,
                sep=None,
                engine="python",
                decimal=decimal
            )

        elif extension in [".xls", ".xlsx"]:
            df = pd.read_excel(file)

        else:
            raise ValueError("Format non supporté (.csv, .xlsx uniquement)")

        if df.empty:
            raise ValueError("Le fichier est vide")

        return df

    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier : {e}")
    
    
def generate_graph(df, plot_type=None, fond_choice=None, title_choice=None, x_label=None, y_label=None, show_regression=False):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import ScalarFormatter
    def clean_to_float(val):
        """Convert a value to float, tolerating whitespace (including non-breaking) and the comma decimal."""
        if pd.isna(val):
            return np.nan
        val = str(val).replace(" ", "").replace("\xa0", "")
        val = val.replace(",", ".")
        try:
            return float(val)
        except ValueError:
            return np.nan
        
    def aggregate_by_x(df, x_col, y_cols, agg="mean"):
        df_agg = (
            df
            .groupby(x_col, as_index=False)[y_cols]
            .agg(agg)
            .sort_values(by=x_col)
            .reset_index(drop=True)
        )
        return df_agg

    # Above ~1000 points, downsample to target ~600 points: rendering stays readable and fast.
    original_len = len(df)
    if original_len > 1000 and plot_type in ["line", "bar", "scatter"]:
        downsample_factor = max(2, original_len // 600)
        df = df.iloc[::downsample_factor].reset_index(drop=True)

    x_col = df.columns[0]
    y_cols = df.columns[1:]

    df[y_cols] = df[y_cols].applymap(clean_to_float)

    if df[x_col].duplicated().any():
        df = aggregate_by_x(df, x_col, y_cols, agg="mean")

    x = df[x_col]
    y_data = df[y_cols]

    max_y = y_data.max().max()
    if pd.isna(max_y) or max_y == 0:
        max_y = 1

    if fond_choice == "Blanc pur":
        figure_facecolor = '#ffffff'
        axes_facecolor = '#ffffff'
        grid_color = '#cccccc'
        text_facecolor = '#222222'
        axes_labelcolor = '#222222'
    elif fond_choice == "Clair doux":
        figure_facecolor = "#dcdeecd5"
        axes_facecolor = "#dcdeecd5"
        grid_color = '#555555'
        text_facecolor = '#222222'
        axes_labelcolor = '#222222'
    elif fond_choice == "Sombre":
        figure_facecolor = '#222222'
        axes_facecolor = '#222222'
        grid_color = '#555555'
        text_facecolor = "#FFFFFF"
        axes_labelcolor = "#FFFFFF"
    else:
        figure_facecolor = '#f5f5f5'
        axes_facecolor = '#f5f5f5'
        grid_color = '#dddddd'
        text_facecolor = '#222222'
        axes_labelcolor = '#222222'


    plt.rcParams.update({
        'figure.facecolor': figure_facecolor,
        'axes.facecolor': axes_facecolor,
        'axes.edgecolor': axes_labelcolor,
        'axes.labelcolor': axes_labelcolor,
        'grid.color': grid_color,
        'font.family': 'DejaVu Sans',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'xtick.color': text_facecolor,
        'ytick.color': text_facecolor,
        'axes.linewidth': 0.8,
        'text.color': text_facecolor,
        'axes.labelcolor': axes_labelcolor,
        'legend.facecolor': axes_facecolor,
        'legend.edgecolor': axes_labelcolor
    })

    fig, ax = plt.subplots(figsize=(10,6))

    if plot_type == "line":
        ax.set_axisbelow(True)
        colors = plt.cm.tab10.colors
        # Above 200 points the markers become unreadable, so we hide them.
        marker_style = 'o' if len(x) < 200 else None
        markersize = 6 if len(x) < 200 else 0

        for i, col in enumerate(y_cols):
            ax.plot(
                x,
                y_data[col],
                marker=marker_style,
                linestyle='-',
                linewidth=2,
                markersize=markersize,
                color=colors[i % len(colors)],
                label=col,
                alpha=0.9
            )

        # ticklabel_format fails silently on non-numeric axes: we let it pass.
        try:
            ax.ticklabel_format(style='plain', axis='y', useOffset=False)
        except:
            pass
        try:
            ax.ticklabel_format(style='plain', axis='x', useOffset=False)
        except:
            pass

        ax.set_ylim(0, max_y * 1.2)
        ax.grid(True, which='major', linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', which='major', length=4, width=1, direction='in')

        if len(x) > 50:
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
                tick.set_ha('right')
            if len(x) > 100:
                ax.locator_params(axis='x', nbins=min(20, len(x)//10))
        else:
            for tick in ax.get_xticklabels():
                tick.set_rotation(30)
                tick.set_ha('right')

        fig.tight_layout()

    elif plot_type == "bar":
        ax.set_axisbelow(True)
        colors = plt.cm.Paired.colors
        if len(y_cols) == 0:
            raise ValueError("Aucune colonne Y détectée pour le graphique")
        width = 0.8 / len(y_cols)
        x_positions = np.arange(len(x))

        for i, col in enumerate(y_cols):
            ax.bar(
                x_positions + i * width,
                y_data[col],
                width=width,
                color=colors[i % len(colors)],
                edgecolor='white',
                linewidth=1,
                label=col,
                alpha=0.9
            )
        
        try:
            ax.ticklabel_format(style='plain', axis='y', useOffset=False)
        except:
            pass
        try:
            ax.ticklabel_format(style='plain', axis='x', useOffset=False)
        except:
            pass
        
        group_centers = x_positions + width * (len(y_cols) - 1) / 2

        # Progressively space out the ticks to avoid label overlap.
        if len(x) > 100:
            step = max(1, len(x) // 20)
            xticks = group_centers[::step]
            xlabels = x[::step]
            rotation = 45

        elif len(x) > 50:
            step = max(1, len(x) // 30)
            xticks = group_centers[::step]
            xlabels = x[::step]
            rotation = 45

        else:
            xticks = group_centers
            xlabels = x
            rotation = 30

        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, rotation=rotation, ha='right')

        ax.set_ylim(0, max_y * 1.2)
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.legend(
            frameon=False,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )

        fig.tight_layout()

    elif plot_type == "scatter":
        ax.set_axisbelow(True)
        colors = plt.cm.tab10.colors
        markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*']
        # Above 500 points, shrink the markers so they don't hide each other.
        point_size = 80 if len(x) < 500 else max(20, 80 - (len(x) // 20))

        for i, col in enumerate(y_cols):
            ax.scatter(
                x,
                y_data[col],
                label=col,
                color=colors[i % len(colors)],
                s=point_size,
                alpha=0.85,
                edgecolor='white',
                linewidth=0.8,
                marker=markers[i % len(markers)]
            )

            if show_regression:
                try:
                    x_numeric = pd.to_numeric(x, errors='coerce')
                    y_numeric = y_data[col]

                    mask = ~(x_numeric.isna() | y_numeric.isna())
                    x_clean = x_numeric[mask]
                    y_clean = y_numeric[mask]

                    if len(x_clean) > 1:
                        z = np.polyfit(x_clean, y_clean, 1)
                        p = np.poly1d(z)

                        x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
                        ax.plot(
                            x_line,
                            p(x_line),
                            "-",
                            color=colors[i % len(colors)],
                            linewidth=2,
                            alpha=0.7,
                            label=f'Régression {col}'
                        )
                    elif len(y_numeric.dropna()) > 0:
                        # Non-numeric X: regression isn't possible, so we display the mean of Y instead.
                        y_mean = y_numeric.mean()
                        ax.axhline(
                            y=y_mean,
                            color=colors[i % len(colors)],
                            linewidth=2,
                            linestyle='--',
                            alpha=0.7,
                            label=f'Moyenne {col}'
                        )
                except Exception as e:
                    try:
                        y_numeric = y_data[col]
                        if len(y_numeric.dropna()) > 0:
                            y_mean = y_numeric.mean()
                            ax.axhline(
                                y=y_mean,
                                color=colors[i % len(colors)],
                                linewidth=2,
                                linestyle='--',
                                alpha=0.7,
                                label=f'Moyenne {col}'
                            )
                    except:
                        pass
                    
        try:
            ax.ticklabel_format(style='plain', axis='y', useOffset=False)
        except:
            pass
        try:
            ax.ticklabel_format(style='plain', axis='x', useOffset=False)
        except:
            pass

        ax.set_ylim(0, max_y * 1.2)
        ax.grid(True, linestyle='--', alpha=0.5)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.legend(
            frameon=False,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )

        fig.tight_layout()

    elif plot_type == "pie":
        colors = plt.cm.Paired.colors

        for i, col in enumerate(y_cols):
            serie = df[col].astype(str).str.replace(" ", "", regex=False)
            serie = pd.to_numeric(serie, errors="coerce")

            valid = ~serie.isna()
            values = serie[valid]
            labels = x[valid]

            if values.empty:
                print(f"⚠️ Impossible de tracer {col} (aucune valeur numérique)")

            else:
                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    pctdistance=0.8,
                    labeldistance=1.05,
                    wedgeprops={'edgecolor': axes_facecolor, 'linewidth': 1.5},
                    textprops={'color': text_facecolor, 'fontsize': 10}
                )

                # Central circle that turns the pie chart into a "donut".
                centre_circle = plt.Circle((0, 0), 0.55, fc=axes_facecolor, alpha=1)
                ax.add_artist(centre_circle)

                ax.set_aspect('equal')

                titre_final = title_choice if 'title_choice' in locals() and title_choice else f"Répartition de {col}"
                ax.set_title(
                    titre_final,
                    pad=15,
                    fontsize=13,
                    fontweight='semibold',
                    color=text_facecolor
                )
                ax.legend(
                    wedges,
                    labels,
                    title=x.name if hasattr(x, "name") else "Catégories",
                    loc="upper left",
                    bbox_to_anchor=(1, 0, 0.5, 1),
                    frameon=False
                )

        fig.tight_layout()
        return fig

    if plot_type != "pie":
        ax.set_title(title_choice, pad=15)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend(
            loc='best',
            frameon=True,
            shadow=True,
            fancybox=True,
            fontsize=10,
            title_fontsize=11
        )
        fig.tight_layout()
        return fig