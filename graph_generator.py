import os
import pandas as pd 
def load_data(file) -> pd.DataFrame:
    def detect_decimal(file, sample_size=5000):
        """
        Detects whether a CSV uses ',' or '.' as decimal separator.
        """
        sample = file.read(sample_size).decode("utf-8", errors="ignore")
        file.seek(0)  # IMPORTANT: reset pointer

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
        """Convertit proprement une valeur en float, même si elle contient espaces/virgules."""
        if pd.isna(val):
            return np.nan
        val = str(val).replace(" ", "").replace("\xa0", "")  # supprime espaces et insécables
        val = val.replace(",", ".")  # remplace les virgules par des points
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

    # === OPTIMIZATION FOR LARGE DATASETS ===
    original_len = len(df)

    if original_len > 1000 and plot_type in ["line", "bar", "scatter"]:
        # Calculate downsample factor to get around 500-800 points
        downsample_factor = max(2, original_len // 600)
        df = df.iloc[::downsample_factor].reset_index(drop=True)

    # graphe
    x_col = df.columns[0]  # première colonne pour l'axe X
    y_cols = df.columns[1:]  # toutes les autres colonnes pour l'axe Y
    
    df[y_cols] = df[y_cols].applymap(clean_to_float)

    if df[x_col].duplicated().any():
        df = aggregate_by_x(df, x_col, y_cols, agg="mean")

    x = df[x_col]
    y_data = df[y_cols]

    max_y = y_data.max().max()
    if pd.isna(max_y) or max_y == 0:
        max_y = 1


    # Définition des couleurs selon le choix
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
    else:  # fallback
        figure_facecolor = '#f5f5f5'
        axes_facecolor = '#f5f5f5'
        grid_color = '#dddddd'
        text_facecolor = '#222222'
        axes_labelcolor = '#222222'


    # === Style global moderne ===
    plt.rcParams.update({
        'figure.facecolor': figure_facecolor,
        'axes.facecolor': axes_facecolor,
        'axes.edgecolor': axes_labelcolor,      # axes eux-mêmes
        'axes.labelcolor': axes_labelcolor, 
        'grid.color': grid_color,
        'font.family': 'DejaVu Sans',      # Police moderne, claire et bien proportionnée
        'font.size': 11,                   # Taille lisible
        'axes.titlesize': 14,              # Taille du titre du graphe
        'axes.labelsize': 12,              # Taille des labels des axes
        'legend.fontsize': 10,             # Taille de la légende
        'xtick.labelsize': 10,             # Taille des ticks en X
        'ytick.labelsize': 10, 
        'xtick.color': text_facecolor,           # ticks X
        'ytick.color': text_facecolor,            # Taille des ticks en Y
        'axes.linewidth': 0.8,             
        'text.color': text_facecolor,           # Texte légèrement assombri
        'axes.labelcolor': axes_labelcolor,
        'legend.facecolor': axes_facecolor,      # fond légende
        'legend.edgecolor': axes_labelcolor
    })

    # === Création du graphique ===
    fig, ax = plt.subplots(figsize=(10,6))

    # GRAPHIQUE EN COURBE
    if plot_type == "line":
        ax.set_axisbelow(True)
        colors = plt.cm.tab10.colors  # 10 couleurs distinctes
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

        # Appliquer ScalarFormatter uniquement si l'axe est numérique
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
            # Reduce number of x-ticks for very large datasets
            if len(x) > 100:
                ax.locator_params(axis='x', nbins=min(20, len(x)//10))
        else:
            for tick in ax.get_xticklabels():
                tick.set_rotation(30)
                tick.set_ha('right')

        fig.tight_layout()

    # GRAPHIQUE EN BARRE
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

        # --- LOGIQUE ADAPTATIVE DES TICKS ---
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

        # Marges et style du graphe
        ax.set_ylim(0, max_y * 1.2)
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        

        # Retirer les bordures pour un rendu “flat”
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Légende propre et déportée
        ax.legend(
            frameon=False,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )

        fig.tight_layout()

    # GRAPHIQUE EN NUAGE DE POINTS
    elif plot_type == "scatter":
        ax.set_axisbelow(True)
        colors = plt.cm.tab10.colors  # palette vive et cohérente
        markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*']
        point_size = 80 if len(x) < 500 else max(20, 80 - (len(x) // 20))

        for i, col in enumerate(y_cols):
            ax.scatter(
                x,
                y_data[col],
                label=col,
                color=colors[i % len(colors)],
                s=point_size,  # taille des points
                alpha=0.85,  # légère transparence
                edgecolor='white',  # contour blanc net
                linewidth=0.8,
                marker=markers[i % len(markers)]
            )

            # Add linear regression line if requested
            if show_regression:
                try:
                    # Try to convert x to numeric
                    x_numeric = pd.to_numeric(x, errors='coerce')
                    y_numeric = y_data[col]
                    
                    # Remove NaN values
                    mask = ~(x_numeric.isna() | y_numeric.isna())
                    x_clean = x_numeric[mask]
                    y_clean = y_numeric[mask]
                    
                    if len(x_clean) > 1:
                        # Calculate linear regression
                        z = np.polyfit(x_clean, y_clean, 1)
                        p = np.poly1d(z)
                        
                        # Plot regression line
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
                        # If x is not numeric but we have y values, show mean line
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
                    # Fallback: try to show mean line if possible
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

        # Marges et limites
        ax.set_ylim(0, max_y * 1.2)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Retirer les bordures
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Légende fluide et externe
        ax.legend(
            frameon=False,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )

        fig.tight_layout()

    # GRAPHIQUE EN CAMAMBERT
    elif plot_type == "pie":
        colors = plt.cm.Paired.colors  # palette douce et contrastée

        for i, col in enumerate(y_cols):
            # Nettoyage et conversion
            serie = df[col].astype(str).str.replace(" ", "", regex=False)
            serie = pd.to_numeric(serie, errors="coerce")

            # Retirer les NaN (valeurs non numériques)
            valid = ~serie.isna()
            values = serie[valid]
            labels = x[valid]

            if values.empty:
                print(f"⚠️ Impossible de tracer {col} (aucune valeur numérique)")

            # === Création du pie chart ===
            else:
                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    pctdistance=0.8,       # pour cent un peu plus proches du bord
                    labeldistance=1.05,    # labels un peu espacés
                    wedgeprops={'edgecolor': axes_facecolor, 'linewidth': 1.5},  # bordures nettes
                    textprops={'color': text_facecolor, 'fontsize': 10}
                )

                # Cercle central pour effet “donut”
                centre_circle = plt.Circle((0, 0), 0.55, fc=axes_facecolor, alpha=1)
                ax.add_artist(centre_circle)

                # Aspect circulaire parfait
                ax.set_aspect('equal')

                titre_final = title_choice if 'title_choice' in locals() and title_choice else f"Répartition de {col}"
                ax.set_title(
                    titre_final,
                    pad=15,
                    fontsize=13,
                    fontweight='semibold',
                    color=text_facecolor
                )
                # Légende externe, propre
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

    # === Mise en forme ===
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