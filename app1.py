import streamlit as st
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page Streamlit
st.set_page_config(page_title="Calculateur de Chargement", layout="wide")

# --- AIDE MÉMOIRE SVG ANIMÉ (BARRE LATÉRALE) ---
st.sidebar.markdown("""
<div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 1rem;">
    <svg viewBox="0 0 500 250" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#1b5e20" /></marker>
            <marker id="arrowhead-start" markerWidth="10" markerHeight="7" refX="1" refY="3.5" orient="auto"><polygon points="10 0, 0 3.5, 10 7" fill="#1b5e20" /></marker>
        </defs>
        <style>
            .cube-front { fill: rgba(129, 199, 132, 0.2); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-top { fill: rgba(129, 199, 132, 0.4); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-side { fill: rgba(129, 199, 132, 0.6); stroke: #388e3c; stroke-width: 2; stroke-linejoin: round; }
            .cube-back { stroke: rgba(56, 142, 60, 0.3); stroke-width: 1.5; stroke-dasharray: 4; fill: none; }
            .dim-line { stroke: #1b5e20; stroke-width: 2; marker-end: url(#arrowhead); marker-start: url(#arrowhead-start); }
            .dim-guide { stroke: rgba(27, 94, 32, 0.4); stroke-width: 1.5; stroke-dasharray: 3; }
            .dim-text { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; font-weight: 700; fill: #1b5e20; }
            @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-8px); } 100% { transform: translateY(0px); } }
            .floating { animation: float 4s ease-in-out infinite; }
        </style>
        <g class="floating">
            <!-- Lignes de fond (transparentes/pointillées) -->
            <polygon points="180,60 380,60 380,140 180,140" class="cube-back" />
            <line x1="120" y1="180" x2="180" y2="140" class="cube-back" />
            <line x1="120" y1="100" x2="180" y2="60" class="cube-back" />
            <!-- Faces du cube -->
            <polygon points="120,100 320,100 380,60 180,60" class="cube-top" />
            <polygon points="320,100 380,60 380,140 320,180" class="cube-side" />
            <polygon points="120,100 320,100 320,180 120,180" class="cube-front" />
            <!-- Guides pointillées pour les flèches -->
            <line x1="120" y1="180" x2="120" y2="210" class="dim-guide" />
            <line x1="320" y1="180" x2="320" y2="210" class="dim-guide" />
            <line x1="120" y1="100" x2="90" y2="100" class="dim-guide" />
            <line x1="120" y1="180" x2="90" y2="180" class="dim-guide" />
            <line x1="320" y1="180" x2="345" y2="195" class="dim-guide" />
            <line x1="380" y1="140" x2="405" y2="155" class="dim-guide" />
            <!-- Flèches de dimension -->
            <line x1="120" y1="205" x2="320" y2="205" class="dim-line" />
            <text x="220" y="228" text-anchor="middle" class="dim-text">Longueur</text>
            <line x1="95" y1="100" x2="95" y2="180" class="dim-line" />
            <text x="80" y="140" text-anchor="middle" transform="rotate(-90 80 140)" class="dim-text">Hauteur</text>
            <line x1="340" y1="190" x2="400" y2="150" class="dim-line" />
            <text x="395" y="190" text-anchor="middle" class="dim-text">Largeur</text>
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# --- MENU MANUEL ---
afficher_manuel = st.sidebar.checkbox("📖 Afficher le manuel d'utilisation")
st.sidebar.markdown("---")

if afficher_manuel:
    st.title("📖 Manuel d'Utilisation")
    st.info("👉 Décochez la case '📖 Afficher le manuel d'utilisation' dans le menu à gauche pour revenir au calculateur.")
    st.markdown("""
    ## 1. Comprendre l'Interface
    L'application est divisée en deux parties principales :
    * **À gauche (Le panneau de configuration) :** C'est ici que vous renseignez les dimensions du camion et des colis. Il est divisé en blocs de couleurs.
    * **À droite (Les résultats) :** C'est ici qu'apparaissent les schémas (vue de dessus et vue de profil) calculés en temps réel.

    > 💡 **Astuce "Aide-mémoire" :** En haut du menu à gauche, une animation en 3D vous rappelle à quoi correspondent la Longueur, la Largeur et la Hauteur pour éviter toute erreur de saisie !

    ## 2. Étape par Étape : Comment configurer votre chargement ?
    ### 🟦 ÉTAPE 1 : Le Camion (Bloc Bleu)
    Renseignez les dimensions utiles intérieures de votre camion ou remorque (en mètres).

    ### 🟧 ÉTAPE 2 : Les Charges Principales (Bloc Orange)
    C'est la marchandise principale que vous souhaitez charger.
    1. **Choisissez le Mode de remplissage :**
       - **Automatique :** L'algorithme calculera le maximum de charges possibles pour remplir tout l'espace disponible dans le camion.
       - **Manuel :** Si vous devez charger exactement 20 palettes, sélectionnez "Manuel" et tapez "20". L'outil dessinera exactement 20 palettes.
    2. Renseignez les dimensions de cette charge.
    3. **Gerbage max :** Indiquez combien de charges peuvent être empilées les unes sur les autres sans s'écraser (ex: tapez 2 si on ne peut faire que 2 couches).

    ### 🟩 ÉTAPE 3 : Les Conteneurs Secondaires (Bloc Vert) - *Optionnel*
    Si vous devez expédier des conteneurs/colis spécifiques **en plus** de vos charges principales, cochez la case *"J'ai des conteneurs spécifiques..."*.
    * Renseignez la quantité et les dimensions de ces conteneurs. 
    * **Ils seront toujours placés en priorité tout au fond du camion** (dessinés en vert).
    * Vous avez plusieurs tailles de colis différents ? Cliquez sur le bouton **"➕ Ajouter un type"** pour ajouter autant de conteneurs différents que nécessaire !

    ---
    ## 3. Comprendre les Résultats (Panneau de Droite)
    Une fois vos données entrées, l'application calcule automatiquement les deux orientations possibles et **vous affiche directement la plus performante** (celle qui permet de charger le plus de matériel).
    
    Si vous souhaitez tout de même consulter la deuxième option (moins optimale, ou équivalente), vous pouvez cliquer sur le menu déroulant **"👀 Voir l'orientation alternative"** apparu en dessous.

    ### Lire les schémas
    Pour l'option affichée, vous disposez d'un plan technique complet avec deux vues synchronisées :
    1. **Le Plan au sol (Vue de dessus) :** Pour visualiser l'occupation de la surface (le contour rouge représente le plancher du camion).
    2. **Le Plan en hauteur (Vue latérale) :** Juste en dessous, parfaitement alignée. Imaginez que vous regardez le camion de profil. Cela vous permet de vérifier le gerbage (les couches superposées) et l'espace libre jusqu'au plafond (ligne rouge du haut).

    ### ⚠️ Les Alertes (Bandeaux Jaunes et Rouges)
    L'application est intelligente et vous protège contre les erreurs physiques :
    * **Bandeau Jaune :** Si vous autorisez un gerbage de 3 couches, mais que le plafond du camion est trop bas pour que les 3 passent, l'application limitera à 2 couches et affichera un avertissement jaune pour vous l'expliquer.
    * **Bandeau Rouge :** Si l'espace demandé pour les "Conteneurs Secondaires" (Verts) ou "Manuels" dépasse la longueur totale du camion, un message d'erreur rouge bloquera le calcul. Réduisez vos quantités !
    """)
    st.stop() # Arrête l'exécution ici pour masquer le calculateur en dessous

# --- FIN DU MENU MANUEL ---

st.title("🚛 Calculateur d'Optimisation de Chargement")
st.markdown("Réservez de la place pour plusieurs types de conteneurs, et découvrez combien de charges principales peuvent rentrer dans l'espace restant.")

# --- INJECTION CSS GLOBALE ---
st.markdown("""
<style>
/* Block 1: Camion (Bleu) */
div[data-testid="stElementContainer"]:has(#camion-header) + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#camion-header) + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#camion-header) + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#camion-header) + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#camion-header) + div + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#camion-header) + div + div + div div[data-baseweb="input"] input {
    background-color: #e1f5fe !important;
    color: #0277bd !important;
}
div[data-testid="stElementContainer"]:has(#camion-header) + div button,
div[data-testid="stElementContainer"]:has(#camion-header) + div + div button,
div[data-testid="stElementContainer"]:has(#camion-header) + div + div + div button {
    background-color: #b3e5fc !important;
    color: #0277bd !important;
}
/* Block 2: Charges Principales (Orange) */
div[data-testid="stElementContainer"]:has(#charges-header) + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div + div div[data-baseweb="input"] input,
div[data-testid="stElementContainer"]:has(#contraintes-header) + div div[data-baseweb="input"],
div[data-testid="stElementContainer"]:has(#contraintes-header) + div div[data-baseweb="input"] input {
    background-color: #fff3e0 !important;
    color: #e65100 !important;
}
div[data-testid="stElementContainer"]:has(#charges-header) + div button,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div button,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div button,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div button,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div button,
div[data-testid="stElementContainer"]:has(#charges-header) + div + div + div + div + div + div button,
div[data-testid="stElementContainer"]:has(#contraintes-header) + div button {
    background-color: #ffe0b2 !important;
    color: #e65100 !important;
}
div[data-testid="stElementContainer"]:has(#charges-header) + div label {
    color: #e65100 !important;
}

/* Customisation de la case à cocher principale (Vert) */
div[data-testid="stElementContainer"]:has(#conteneurs-header) + div div[data-testid="stCheckbox"] {
    background-color: #e8f5e9 !important;
    padding: 8px 10px;
    border-radius: 5px;
}
div[data-testid="stElementContainer"]:has(#conteneurs-header) + div div[data-testid="stCheckbox"] p {
    color: #1b5e20 !important;
    font-weight: bold;
}
/* Customisation des boutons d'ajout/retrait de conteneurs */
div[data-testid="stElementContainer"]:has(#cont-buttons) + div button {
    background-color: #c8e6c9 !important;
    color: #1b5e20 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ÉTAT ---
if 'nb_conteneurs' not in st.session_state:
    st.session_state.nb_conteneurs = 1

# --- BARRE LATÉRALE : ENTRÉES UTILISATEUR ---

# BLOC 1 : CAMION (Bleu)
st.sidebar.markdown("""
<div id="camion-header" style="background-color: #e1f5fe; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
    <h4 style="margin:0; color: #0277bd;">📏 Dimensions du Camion</h4>
</div>
""", unsafe_allow_html=True)

camion_L = st.sidebar.number_input("Longueur du plancher", min_value=1.0, value=13.5, step=0.1)
camion_l = st.sidebar.number_input("Largeur du plancher", min_value=1.0, value=2.4, step=0.1)
camion_h = st.sidebar.number_input("Hauteur utile max", min_value=1.0, value=2.7, step=0.1)

# BLOC 2 : CHARGES PRINCIPALES (Orange)
st.sidebar.markdown("""
<div id="charges-header" style="background-color: #fff3e0; padding: 10px; border-radius: 5px; margin-bottom: 10px; margin-top: 15px;">
    <h4 style="margin:0; color: #e65100;">📦 Charges Principales</h4>
</div>
""", unsafe_allow_html=True)

# -- CHOIX DU MODE AUTOMATIQUE OU MANUEL --
mode_calcul = st.sidebar.radio(
    "Mode de remplissage",
    options=["Automatique (Remplir l'espace)", "Manuel (Quantité exacte)"],
    index=0
)

if mode_calcul == "Manuel (Quantité exacte)":
    qte_principale_demandee = st.sidebar.number_input("Nombre exact de charges à placer", min_value=0, value=20, step=1)
else:
    qte_principale_demandee = -1 # Signifie "Illimité / Automatique"

charge_L = st.sidebar.number_input("Longueur de la charge", min_value=0.01, value=1.00, step=0.01)
charge_l = st.sidebar.number_input("Largeur de la charge", min_value=0.01, value=1.20, step=0.01)
charge_h = st.sidebar.number_input("Hauteur de la charge", min_value=0.01, value=0.62, step=0.01)

st.sidebar.markdown('<div id="contraintes-header" style="margin-top: 10px; margin-bottom: 5px;"><strong>⚙️ Contraintes</strong></div>', unsafe_allow_html=True)
gerbage_autorise = st.sidebar.number_input("Gerbage max (Combien de charges empilées max ?)", min_value=1, value=3, step=1)

# BLOC 3 : CONTENEURS (Vert) DYNAMIQUE
st.sidebar.markdown("""
<div id="conteneurs-header" style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin-bottom: 10px; margin-top: 15px;">
    <h4 style="margin:0; color: #1b5e20;">🧮 Conteneurs Secondaires</h4>
</div>
""", unsafe_allow_html=True)

inclure_conteneurs = st.sidebar.checkbox("J'ai des conteneurs spécifiques à charger absolument", value=True)

conteneurs_data = []

if inclure_conteneurs:
    # Liste des couleurs qui seront appliquées au graphique ET aux champs de saisie
    couleurs_vert = ["#b9f6ca", "#69f0ae", "#00e676", "#00c853", "#a5d6a7", "#81c784"]
    dynamic_css = "<style>\n"
    
    for i in range(st.session_state.nb_conteneurs):
        color = couleurs_vert[i % len(couleurs_vert)]
        
        # Affichage du header coloré de la même couleur que le graphique
        st.sidebar.markdown(f"""
        <div id='cont-type-{i}' style='background-color: {color}; padding: 5px 10px; border-radius: 5px; margin-top: 15px; margin-bottom: 5px; color: #000; border: 1px solid rgba(0,0,0,0.1);'>
            <b>📦 Type {i+1}</b>
        </div>
        """, unsafe_allow_html=True)
        
        # Le type 1 a 14 par défaut, les types 2+ ont 0 par défaut
        default_qte = 14 if i == 0 else 0
            
        cont_qte = st.sidebar.number_input(f"Nombre de conteneurs", min_value=0, value=default_qte, step=1, key=f"qte_{i}")
        cont_L = st.sidebar.number_input(f"Longueur du conteneur", min_value=0.01, value=2.25, step=0.01, key=f"L_{i}")
        cont_l = st.sidebar.number_input(f"Largeur du conteneur", min_value=0.01, value=1.50, step=0.01, key=f"l_{i}")
        cont_h = st.sidebar.number_input(f"Hauteur du conteneur", min_value=0.01, value=0.92, step=0.01, key=f"h_{i}")
        cont_gerbage = st.sidebar.number_input(f"Gerbage max conteneurs", min_value=1, value=2, step=1, key=f"gerb_{i}")
        
        conteneurs_data.append({
            "qte": cont_qte, "L": cont_L, "l": cont_l, "h": cont_h, "gerbage": cont_gerbage,
            "color": color
        })
        
        # CSS dynamique ciblant spécifiquement les 5 champs qui suivent ce Type précis
        dynamic_css += f"""
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div div[data-baseweb="input"],
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div div[data-baseweb="input"] input,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div div[data-baseweb="input"],
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div div[data-baseweb="input"] input,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div div[data-baseweb="input"],
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div div[data-baseweb="input"] input,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div div[data-baseweb="input"],
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div div[data-baseweb="input"] input,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div + div div[data-baseweb="input"],
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div + div div[data-baseweb="input"] input {{
            background-color: {color} !important;
            color: #000000 !important;
        }}
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div button,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div button,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div button,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div button,
        div[data-testid="stElementContainer"]:has(#cont-type-{i}) + div + div + div + div + div button {{
            background-color: rgba(255,255,255,0.4) !important;
            color: #000000 !important;
        }}
        """
        
    dynamic_css += "</style>"
    st.markdown(dynamic_css, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div id='cont-buttons'></div>", unsafe_allow_html=True)
    col1, col2 = st.sidebar.columns(2)
    if col1.button("➕ Ajouter un type"):
        st.session_state.nb_conteneurs += 1
        st.rerun()
    if st.session_state.nb_conteneurs > 1:
        if col2.button("➖ Retirer type"):
            st.session_state.nb_conteneurs -= 1
            st.rerun()

# --- 1. CALCUL DE L'ESPACE PRIS PAR LES CONTENEURS FIXES ---
longueur_amputee_totale = 0
conteneurs_places = []
erreur_conteneurs = False

if inclure_conteneurs:
    for cont in conteneurs_data:
        if cont["qte"] > 0:
            c_couches = min(math.floor(camion_h / cont["h"]), cont["gerbage"])
            if c_couches > 0:
                places_sol = math.ceil(cont["qte"] / c_couches)
                
                # Test Orientation A
                nb_l_A = math.floor(camion_l / cont["l"])
                len_A = math.ceil(places_sol / nb_l_A) * cont["L"] if nb_l_A > 0 else float('inf')
                
                # Test Orientation B
                nb_l_B = math.floor(camion_l / cont["L"])
                len_B = math.ceil(places_sol / nb_l_B) * cont["l"] if nb_l_B > 0 else float('inf')
                
                if len_A <= len_B and len_A != float('inf'):
                    l_amp = len_A
                    c_rangees = math.ceil(places_sol / nb_l_A)
                    c_largeur = nb_l_A
                    c_dim_x = cont["L"]
                    c_dim_y = cont["l"]
                elif len_B != float('inf'):
                    l_amp = len_B
                    c_rangees = math.ceil(places_sol / nb_l_B)
                    c_largeur = nb_l_B
                    c_dim_x = cont["l"]
                    c_dim_y = cont["L"]
                else:
                    l_amp = float('inf')
                    erreur_conteneurs = True
            else:
                l_amp = float('inf')
                erreur_conteneurs = True

            if not erreur_conteneurs:
                conteneurs_places.append({
                    "l_amp": l_amp, "rangees": c_rangees, "largeur": c_largeur,
                    "dim_x": c_dim_x, "dim_y": c_dim_y, "couches": c_couches,
                    "qte_sol": places_sol, "h": cont["h"], "color": cont["color"]
                })
                longueur_amputee_totale += l_amp

L_dispo = round(max(0.0, camion_L - longueur_amputee_totale), 2)

# --- 2. CALCUL DES CHARGES PRINCIPALES DANS L'ESPACE RESTANT ---
couches_possibles_hauteur = math.floor(camion_h / charge_h)
couches_reelles = min(couches_possibles_hauteur, gerbage_autorise)

qte_opt1 = qte_opt2 = 0
rangees1 = largeur1 = rangees2 = largeur2 = 0
erreur_manuelle_opt1 = erreur_manuelle_opt2 = False

if L_dispo >= 0 and not erreur_conteneurs and longueur_amputee_totale <= camion_L:
    # Scénario A (Orientation 1)
    max_L1 = math.floor(L_dispo / charge_L)
    max_l1 = math.floor(camion_l / charge_l)
    capa_max_1 = max_L1 * max_l1 * couches_reelles
    
    if mode_calcul == "Automatique (Remplir l'espace)":
        qte_opt1 = capa_max_1
    else:
        qte_opt1 = min(qte_principale_demandee, capa_max_1)
        if qte_principale_demandee > capa_max_1: erreur_manuelle_opt1 = True
        
    if qte_opt1 > 0:
        spots1 = math.ceil(qte_opt1 / couches_reelles)
        rangees1 = math.ceil(spots1 / max_l1) if max_l1 > 0 else 0
        largeur1 = max_l1

    # Scénario B (Orientation 2)
    max_L2 = math.floor(L_dispo / charge_l)
    max_l2 = math.floor(camion_l / charge_L)
    capa_max_2 = max_L2 * max_l2 * couches_reelles
    
    if mode_calcul == "Automatique (Remplir l'espace)":
        qte_opt2 = capa_max_2
    else:
        qte_opt2 = min(qte_principale_demandee, capa_max_2)
        if qte_principale_demandee > capa_max_2: erreur_manuelle_opt2 = True
        
    if qte_opt2 > 0:
        spots2 = math.ceil(qte_opt2 / couches_reelles)
        rangees2 = math.ceil(spots2 / max_l2) if max_l2 > 0 else 0
        largeur2 = max_l2

# --- FONCTIONS DE DESSIN RESPONSIVES ET VERROUILLÉES ---
def dessiner_plan(qte_totale, couches, rangees, largeur, dim_x, dim_y, titre):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=camion_L, y1=camion_l,
                  line=dict(color="red", width=3), fillcolor="rgba(0,0,0,0)")

    # Dessiner les charges principales exactement selon la quantité demandée
    if qte_totale > 0:
        spots_to_draw = math.ceil(qte_totale / couches)
        for i in range(rangees):
            for j in range(largeur):
                if spots_to_draw > 0:
                    x0 = i * dim_x
                    y0 = j * dim_y
                    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+dim_x, y1=y0+dim_y,
                                  line=dict(color="black", width=1), fillcolor="skyblue")
                    spots_to_draw -= 1

    # Dessiner les conteneurs fixes
    if inclure_conteneurs and longueur_amputee_totale <= camion_L and not erreur_conteneurs:
        current_start_x = camion_L 
        for cp in conteneurs_places:
            start_x = current_start_x - cp["l_amp"]
            spots_to_draw = cp["qte_sol"]
            for i in range(cp["rangees"]):
                for j in range(cp["largeur"]):
                    if spots_to_draw > 0:
                        x0 = start_x + i * cp["dim_x"]
                        y0 = j * cp["dim_y"]
                        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+cp["dim_x"], y1=y0+cp["dim_y"],
                                      line=dict(color="black", width=1, dash="dot"), fillcolor=cp["color"])
                        spots_to_draw -= 1
            current_start_x = start_x

    fig.update_layout(
        title=titre, 
        xaxis=dict(
            title="Longueur Camion (m)", 
            range=[-0.5, camion_L + 0.5], 
            autorange=False, 
            constrain='domain',
            fixedrange=True
        ),
        yaxis=dict(
            title="Largeur Camion (m)", 
            range=[-0.5, max(camion_l, 3.0) + 0.5], 
            scaleanchor="x", 
            scaleratio=1, 
            autorange=False, 
            constrain='domain',
            fixedrange=True
        ),
        autosize=True, 
        height=400, 
        plot_bgcolor="white", 
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def dessiner_vue_laterale(qte_totale, couches, rangees, largeur, dim_x, dim_h, titre):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=camion_L, y1=camion_h,
                  line=dict(color="red", width=3), fillcolor="rgba(0,0,0,0)")

    # Dessiner les charges principales
    if qte_totale > 0:
        items_left = qte_totale
        for i in range(rangees):
            if items_left <= 0: break
            items_in_this_row = min(items_left, largeur * couches)
            layers_in_this_row = math.ceil(items_in_this_row / largeur)
            
            for k in range(layers_in_this_row):
                x0 = i * dim_x
                y0 = k * dim_h
                fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+dim_x, y1=y0+dim_h,
                              line=dict(color="black", width=1), fillcolor="skyblue")
            items_left -= items_in_this_row

    # Dessiner les conteneurs fixes
    if inclure_conteneurs and longueur_amputee_totale <= camion_L and not erreur_conteneurs:
        current_start_x = camion_L
        for cp in conteneurs_places:
            start_x = current_start_x - cp["l_amp"]
            for i in range(cp["rangees"]):
                for k in range(cp["couches"]):
                    x0 = start_x + i * cp["dim_x"]
                    y0 = k * cp["h"]
                    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0+cp["dim_x"], y1=y0+cp["h"],
                                  line=dict(color="black", width=1, dash="dot"), fillcolor=cp["color"])
            current_start_x = start_x

    fig.update_layout(
        title=titre, 
        xaxis=dict(
            title="Longueur Camion (m)", 
            range=[-0.5, camion_L + 0.5], 
            autorange=False, 
            constrain='domain',
            fixedrange=True
        ),
        yaxis=dict(
            title="Hauteur Camion (m)", 
            range=[-0.5, max(camion_h, 3.0) + 0.5], 
            scaleanchor="x", 
            scaleratio=1, 
            autorange=False, 
            constrain='domain',
            fixedrange=True
        ),
        autosize=True, 
        height=350, 
        plot_bgcolor="white", 
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# --- AFFICHAGE DES RÉSULTATS ---
st.header("📊 Résultats de l'optimisation")

if erreur_conteneurs or longueur_amputee_totale > camion_L:
    st.error(f"⚠️ Impossible ! L'ensemble des conteneurs prend plus de place que le camion (ou ne rentre pas en hauteur).")
else:
    # --- ALERTE PLAFOND (CHARGES PRINCIPALES) ---
    if couches_possibles_hauteur < gerbage_autorise:
        st.warning(f"⚠️ **Plafond atteint (Charges Principales) :** Vous avez autorisé un gerbage de {gerbage_autorise}, mais la hauteur du camion ({camion_h}m) limite physiquement l'empilement à **{couches_reelles} couches** (de {charge_h}m de haut).")

    # --- ALERTE PLAFOND (CONTENEURS) ---
    if inclure_conteneurs:
        for i, cont in enumerate(conteneurs_data):
            if cont["qte"] > 0:
                c_pos = math.floor(camion_h / cont["h"])
                if c_pos < cont["gerbage"] and c_pos > 0:
                    st.warning(f"⚠️ **Plafond atteint (Conteneurs Type {i+1}) :** Vous avez autorisé un gerbage de {cont['gerbage']}, mais la hauteur du camion limite l'empilement à **{c_pos} couches**.")

    if inclure_conteneurs:
        qte_totale_cont = sum(c["qte"] for c in conteneurs_data)
        if qte_totale_cont > 0:
            st.info(f"🚚 **Espace réservé au fond :** Les {qte_totale_cont} conteneurs prennent **{longueur_amputee_totale} m** de long au sol. Il reste **{L_dispo} m** pour les charges principales.")

    # Déterminer la meilleure option pour l'affichage principal
    if qte_opt1 >= qte_opt2:
        best_opt, alt_opt = 1, 2
        best_qte, best_rangees, best_largeur, best_dim_L, best_dim_l, best_err = qte_opt1, rangees1, largeur1, charge_L, charge_l, erreur_manuelle_opt1
        alt_qte, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, alt_err = qte_opt2, rangees2, largeur2, charge_l, charge_L, erreur_manuelle_opt2
    else:
        best_opt, alt_opt = 2, 1
        best_qte, best_rangees, best_largeur, best_dim_L, best_dim_l, best_err = qte_opt2, rangees2, largeur2, charge_l, charge_L, erreur_manuelle_opt2
        alt_qte, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, alt_err = qte_opt1, rangees1, largeur1, charge_L, charge_l, erreur_manuelle_opt1

    # --- AFFICHAGE DE LA MEILLEURE OPTION ---
    st.subheader(f"🌟 Orientation Recommandée (Option {best_opt})")
    
    if best_err:
        st.warning(f"⚠️ L'espace restant est insuffisant pour placer vos {qte_principale_demandee} charges. Le maximum possible a été affiché.")
        
    st.metric(label="Total de charges principales", value=f"{best_qte} charges")
    if best_qte > 0:
        st.write(f"- Jusqu'à **{best_rangees}** rangées dans la longueur")
        st.write(f"- Jusqu'à **{best_largeur}** charges côte à côte")
        st.write(f"- Jusqu'à **{couches_reelles}** charges superposées en hauteur")
    
    # Affichage des graphiques empilés verticalement pour une adaptabilité parfaite
    fig_best_dessus = dessiner_plan(best_qte, couches_reelles, best_rangees, best_largeur, best_dim_L, best_dim_l, "Plan au sol (Vue de dessus)")
    st.plotly_chart(fig_best_dessus, use_container_width=True, key="chart_best_dessus")

    fig_best_cote = dessiner_vue_laterale(best_qte, couches_reelles, best_rangees, best_largeur, best_dim_L, charge_h, "Plan en hauteur (Vue latérale)")
    st.plotly_chart(fig_best_cote, use_container_width=True, key="chart_best_cote")

    # --- AFFICHAGE CACHÉ DE L'OPTION ALTERNATIVE ---
    titre_expander = "👀 Voir l'orientation alternative (Résultat équivalent)" if qte_opt1 == qte_opt2 else "👀 Voir l'orientation alternative (Moins optimale)"
    
    with st.expander(titre_expander):
        st.markdown(f"**Option {alt_opt}**")
        if alt_err:
            st.warning(f"⚠️ L'espace restant est insuffisant pour placer vos {qte_principale_demandee} charges. Le maximum possible a été affiché.")
            
        st.metric(label="Total de charges principales", value=f"{alt_qte} charges")
        if alt_qte > 0:
            st.write(f"- Jusqu'à **{alt_rangees}** rangées dans la longueur")
            st.write(f"- Jusqu'à **{alt_largeur}** charges côte à côte")
            st.write(f"- Jusqu'à **{couches_reelles}** charges superposées en hauteur")
            
        fig_alt_dessus = dessiner_plan(alt_qte, couches_reelles, alt_rangees, alt_largeur, alt_dim_L, alt_dim_l, "Plan au sol (Vue de dessus)")
        st.plotly_chart(fig_alt_dessus, use_container_width=True, key="chart_alt_dessus")

        fig_alt_cote = dessiner_vue_laterale(alt_qte, couches_reelles, alt_rangees, alt_largeur, alt_dim_L, charge_h, "Plan en hauteur (Vue latérale)")
        st.plotly_chart(fig_alt_cote, use_container_width=True, key="chart_alt_cote")