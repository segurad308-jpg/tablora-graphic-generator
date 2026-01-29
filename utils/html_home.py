import streamlit as st

@st.cache_data
def render_static_home():
    return """
    <div class="hero-section">
        <a class="hero-catch" href="/Offre" target="_self">
            <div class="hero-catch-left">ㅤN°1ㅤ</div>
            <div class="hero-catch-mid">ㅤTablora pour Créer et Personnaliser Vos Graphiques  ㅤ</div>
            <div class="hero-catch-right">‎ ‎  🡪 ‎ ‎ </div>
        </a>
        <div class="hero-title">Crée et Personnalise tes Graphiques Rapidement et Facilement</div>
        <div class="hero-desc">
            Vous êtes étudiant ou professionnel et vous avez régulièrement besoin de créer des graphiques <br>
                mais vous trouvez ce processus long et complexe ?<br>
                Grâce à Tablora, élaborez vos graphiques en seulement quelques clics
        </div>
        <div style="display: flex; gap: 20px; margin-top: 30px; margin-bottom: 20px;">
            <a href="/Offre" target="_self" class="neumo-btn1">
                Essayer gratuitement
            </a>
            <a href="/Offre" target="_self" class="neumo-btn">
                Voir l'offre
            </a> 
        </div>
        <div class="hero-sub">
            ★ ‎ ★ ‎ ★ ‎ ★ ‎ ★ㅤ<u>De nombreux utilisateurs satisfaits</u>
        </div>
    </div>

    <div class="neumo-card">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/design.webp?raw=true" class="neumo-img" alt="Feature">
        <div style="display: flex; flex-direction: column; width: 50%;">
            <div class="st1">
                Visualisez plus vite et mieux<br> 
                avec 
                <span style="color:#603CC9;">Tablora</span>
            </div>
            <div class="neumo-text">
                Générez des graphiques époustouflants en seulement quelques secondes grâce à notre interface intuitive.
            </div>
            <a href="/Offre" target="_self" class="neumo-btn1">
                Essayer maintenant
            </a>
        </div>
    </div>

    <div class="st2">
        <div style="text-align: center;">
            Tablora explore et visualise vos données<br>
            en un clin d'œil
        </div>
    </div>

    <div class="neumo-row">
    <div class="feature-card">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre.webp?raw=true" class="feature-image" />
        <div class="feature-title">Importez vos données CSV et Excel</div>
        <div class="feature-desc">Importez en un clic vos tableau de données.</div>
    </div>

    <div class="feature-card">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/his.webp?raw=true" class="feature-image" />
        <div class="feature-title">Créez des graphes personnalisables et rapides</div>
        <div class="feature-desc">Choisissez le graphe qui vous correspond le mieux.</div>
    </div>

    <div class="feature-card">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre%20(1).webp?raw=true" class="feature-image" />
        <div class="feature-title">Téléchargement pro</div>
        <div class="feature-desc">Exportez en PNG, PDF, SVG et partagez vos créations partout.</div>
    </div>

    <div class="feature-card">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre%20(2).webp?raw=true" class="feature-image" />
        <div class="feature-title">Données sécurisées</div>
        <div class="feature-desc">Vos fichiers ne quittent jamais votre ordinateur et ne sont pas stockés.</div>
    </div>
    </div>

    <div class='gradient-section'>
        <div class="bottom-section">
            <div class="bottom-left">
                <div class="st1">Qui sommes-nous ?</div>
                <div class="bottom-desc">
                    <span style="color:#603CC9;">Tablora</span> est une entreprise Suisse, ayant conçu un outil de visualisation de données pour les étudiants et les professionnels.
                    Notre mission est de rendre la création de graphiques accessible à tous, en simplifiant le processus qui parfois peut sembler complexe.<br><br>
                    La conception de graphiques prend souvent du temps et nécessite des compétences techniques et par conséquent,
                    nous cherchons à faciliter la tâche aux personnes souhaitant représenter visuellement leurs données.<br>
                    Avec <span style="color:#603CC9;">Tablora</span>, ménagez vos efforts et transformez vos données en visualisations percutantes en seulement quelques clics.
                </div>
            </div>
            <div class="bottom-right">
                <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/travail.webp?raw=true" class="bottom-img" alt="Demo" />
            </div>
        </div>
    </div>
    <div class='separator'></div>

    <div class="st2">
        <div style="justify-content: center;">
            Pourquoi choisir Tablora ?
        </div>
    </div> 

    <div class="neumo-container">
    <table class="neumo-table">
    <tr>
        <th style="color:#311566;">Avantages</th>
        <th style="text-align:center;color:#603CC9;">Tablora</th>
        <th style="text-align:center;color:#311566;">&copy; Tableau Software</th>
        <th style="text-align:center;color:#311566;">&copy; Excel</th>
    </tr>

    <tr>
        <td>Rapide et intuitif</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">-</td>
        <td class="neumo-check">✔</td>
    </tr>

    <tr>
        <td>Visualisation puissante</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">-</td>
    </tr>

    <tr>
        <td>Personnalisation facile</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">-</td>
    </tr>

    <tr>
        <td>Téléchargement haute qualité</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">-</td>
    </tr>

    <tr>
        <td>Abordable et accessible</td>
        <td class="neumo-check">✔</td>
        <td class="neumo-check">-</td>
        <td class="neumo-check">✔</td>
    </tr>
    </table>
    </div>

    <div class="st2">
        <div style="justify-content: center;">
            Questions fréquentes
        </div>
    </div>
    """

@st.cache_data
def render_static_home2():
    return """
    <section class="reviews-section">
        <div class="st4">Avis</div>
        <div class="reviews-grid">
                
    <div class="review-card">
        <div class="review-header">
            <div class="review-avatar">Q</div>
            <div class="review-meta">
                <div class="review-name">Quentin S.</div>
                <div class="review-stars">★★★★★</div>
            </div>
        </div>
        <div class="review-text">J'ai été impressionné par la facilité d'utilisation du logiciel. J'ai l'habitude
                de créer des graphiques et par conséquent j'étais sceptique à l'idée d'utiliser Tablora, car c'est en général une tâche
                laborieuse et complexe. J'ai fait mon choix et je ne reviendrai pas en arrière.</div>
    </div>

    <div class="review-card">
        <div class="review-header">
            <div class="review-avatar">D</div>
            <div class="review-meta">
                <div class="review-name">David L.</div>
                <div class="review-stars">★★★★★</div>
            </div>
        </div>
        <div class="review-text">Tout simplement j'adore ! J'aurais jamais cru que ce serait autant facile de créer des
                graphiques mais avec Tablora j'ai qu'à cliquer sur quelques boutons et le tour est joué !
                Si vous avez besoin de créer des graphiques rapidement, je recommande fortement Tablora.</div>
    </div>

    <div class="review-card">
        <div class="review-header">
            <div class="review-avatar">C</div>
            <div class="review-meta">
                <div class="review-name">Catherine M.</div>
                <div class="review-stars">★★★★☆</div>
            </div>
        </div>
        <div class="review-text">Cela a toujours été pour moi une tâche compliquée, et donc en trouvant ce logiciel, 
                j'ai pu facilement créer de bons graphiques sans effort. De cette manière, je peux maintenant facilement 
                intégrer des graphiques à mes présentations lors de mes projets d'étude.</div>
    </div>

    </div>
    <div class="review-submit-card">
        <div class="st3">Donner votre avis</div>

    <form action="https://formspree.io/f/mkojrbjk" method="POST" class="review-form">

    <!-- Ligne du haut -->
    <div class="review-top">
    <input type="text" name="Nom" placeholder="Votre nom" required>

    <div class="star-rating">
    <input type="radio" id="star5" name="Note" value="5" required>
    <label for="star5">★</label>

    <input type="radio" id="star4" name="Note" value="4">
    <label for="star4">★</label>

    <input type="radio" id="star3" name="Note" value="3">
    <label for="star3">★</label>

    <input type="radio" id="star2" name="Note" value="2">
    <label for="star2">★</label>

    <input type="radio" id="star1" name="Note" value="1">
    <label for="star1">★</label>
    </div>
    </div>

    <!-- Avis -->
    <textarea name="Avis" rows="3" placeholder="Votre avis" required></textarea>

    <button type="submit">Publier mon avis</button>
    </form>
    </div>

    </section>

    <div class="banner">
        <div class="banner-text">
                Commencez gratuitement dès aujourd'hui !
        </div>
    </div>

    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 0; text-align: center;">
        <a href="/Offre" target="_self" class="neumo-btn2">
            Essayer gratuitement
        </a>
        <a href="/Offre" target="_self" class="neumo-btn3">
            Acheter l'offre maintenant
        </a>
    </div>
    """
