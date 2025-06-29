import streamlit as st # type: ignore
from fpdf import FPDF # type: ignore
import datetime

# 🔒 Fonction de nettoyage texte pour PDF
def safe_text(text):
    return str(text).replace("–", "-").replace("’", "'").replace("•", "-").replace("✅", "").replace("📋", "").replace("📄", "").replace("🔁", "").replace("🔍", "").replace("📝", "").replace("📥", "")

# 🔵 Fonction d'affichage avec classe AHA
def afficher_recommandation_aha(texte, classe):
    if classe == "1":
        st.success(f"🟢 Classe 1 – {texte}")
    elif classe == "2a":
        st.info(f"🟡 Classe 2a – {texte}")
    elif classe == "2b":
        st.warning(f"🟠 Classe 2b – {texte}")
    elif classe == "3":
        st.error(f"🔴 Classe 3 – {texte}")

st.set_page_config(page_title="Aide au suivi de la SAS", layout="centered")

st.title("🫀 Évaluation clinique des valvulopathies cardiaques")
st.subheader("Basé sur les recommandations AHA/ACC 2020")

type_valvulopathie = st.selectbox(
    "Choisir la valvulopathie à évaluer :",
    ["Sténose aortique (SAS)", "Insuffisance aortique (IA)", "Insuffisance mitrale (IM)", "Sténose mitrale (SM)"]
)

# Étape 1 : SAS confirmée ?
if type_valvulopathie == "Sténose aortique (SAS)":
    st.markdown("### 1. SAS confirmée par échographie ?")
    sas_confirmee = st.radio("SAS confirmée ?", ["Oui", "Non"])

    # Étape 2 : Symptômes
    if sas_confirmee == "Oui":
        st.markdown("### 2. Symptômes présents ?")
        symptomes_sas = st.radio("Symptômes présents ?", ["Oui", "Non"])

        if symptomes_sas == "Oui":
            st.markdown("### 3. Traitement SAS symptomatique")
            risque = st.radio("Risque chirurgical élevé ?", ["Oui", "Non"])
            age = st.number_input("Âge du patient (en années)", min_value=0, max_value=120, step=1)

            if risque == "Oui" or age >= 80:
                afficher_recommandation_aha("TAVI recommandé", "1")
            else:
                afficher_recommandation_aha("SAVR recommandé", "1")

        else:
            st.markdown("### 3. Suivi SAS asymptomatique")
            fegv = st.radio("FEVG < 50% ?", ["Oui", "Non"])
            gradient = st.radio("Gradient > 60 mmHg ?", ["Oui", "Non"])
            vmax_aha = st.radio("Vmax > 5.0 m/s ?", ["Oui", "Non"])

            if fegv == "Oui" or gradient == "Oui" or vmax_aha == "Oui":
                afficher_recommandation_aha("Intervention recommandée", "1")
            else:
                afficher_recommandation_aha("Surveillance échographique", "2a")

    elif sas_confirmee == "Non":
        afficher_recommandation_aha("Surveillance ou réévaluation selon contexte clinique", "2a")

elif type_valvulopathie == "Insuffisance aortique (IA)":
    st.markdown("### 1. Symptômes présents ?")
    symptomes_ia = st.radio("Symptômes présents ?", ["Oui", "Non"])

    st.markdown("### 2. Paramètres échographiques")
    fevg_ia = st.radio("FEVG < 55 % ?", ["Oui", "Non"])
    dtdvg_sup70 = st.radio("Diamètre télédiastolique VG ≥ 70 mm ?", ["Oui", "Non"])

    # 🔎 Analyse des cas
    if symptomes_ia == "Oui":
        afficher_recommandation_aha("Intervention recommandée", "1")
    elif symptomes_ia == "Non" and fevg_ia == "Oui":
        afficher_recommandation_aha("CIntervention recommandée", "1")
    elif symptomes_ia == "Non" and fevg_ia == "Non":
        if dtdvg_sup70 == "Oui":
            afficher_recommandation_aha("Intervention recommandée", "2a")
        else:
            afficher_recommandation_aha("Surveillance échographique", "2b")

elif type_valvulopathie == "Insuffisance mitrale (IM)":
    st.markdown("## 1. Symptômes présents ?")
    symptomes_im = st.radio("Symptômes présents ?", ["Oui", "Non"], key="symptomes_im")

    st.markdown("## 2. FEVG < 60 % ?")
    fevg60 = st.radio("FEVG < 60 % ?", ["Oui", "Non"], key="fevg60")

    # Décision
    if symptomes_im == "Oui":
        afficher_recommandation_aha("Chirurgie recommandée", "1")
    elif symptomes_im == "Non" and fevg60 == "Oui":
        afficher_recommandation_aha("Chirurgie recommandée", "1")
    elif symptomes_im == "Non" and fevg60 == "Non":
        afficher_recommandation_aha("Surveillance échographique", "2a")
    else:
        st.warning("🟠 Données insuffisantes pour établir une recommandation.")

elif type_valvulopathie == "Sténose mitrale (SM)":
    st.markdown("### 1. Symptômes présents ?")
    symptomes_sm = st.radio("Symptômes présents ?", ["Oui", "Non"], key="symptomes_sm")

    # Puis les données cliniques
    st.markdown("### 2. Données cliniques – Sténose mitrale (SM)")
    st.write(f"• Symptômes présents : {symptomes_sm}")

    if symptomes_sm == "Oui":
        reco = "Intervention recommandée"
        classe = "1"
    else:
        reco = "Surveillance échographique"
        classe = "2a"

    st.success(f"Recommandation AHA (Classe {classe}) : {reco}")

st.markdown("---")
st.markdown("### 📝 Synthèse du cas")

# 🔘 Bouton unique avec clé personnalisée
if st.button("Afficher la synthèse", key="btn_synthese"):
    st.markdown("#### Données cliniques")

    # 🔹 Sténose aortique (SAS)
    if type_valvulopathie == "Sténose aortique (SAS)":
        st.write(f"• Valvulopathie : {type_valvulopathie}")
        st.write(f"• SAS confirmée : {sas_confirmee}")
        st.write(f"• Symptômes présents : {symptomes_sas}")

        if symptomes_sas == "Oui":
            if 'risque' in locals() and 'age' in locals():
                st.write(f"• Risque chirurgical élevé : {risque}")
                st.write(f"• Âge du patient : {age} ans")
            else:
                st.write("• Données de risque ou âge non disponibles.")
        else:
            if 'fegv' in locals() and 'gradient' in locals() and 'vmax_aha' in locals():
                st.write(f"• FEVG < 50 % : {fegv}")
                st.write(f"• Gradient > 60 mmHg : {gradient}")
                st.write(f"• Vmax > 5.0 m/s : {vmax_aha}")
            else:
                st.write("• Données asymptomatiques non disponibles.")
        
        # 🔁 Calcul de la recommandation AHA
        if sas_confirmee == "Non":
            reco = "Surveillance ou réévaluation"
        elif symptomes_sas == "Non":
            if fegv == "Oui" or gradient == "Oui" or vmax_aha == "Oui":
                reco = "Intervention recommandée"
            else:
                reco = "Surveillance échographique"
        elif risque == "Oui" or (age is not None and age >= 80):
            reco = "TAVI"
        else:
            reco = "SAVR"

        # Attribution classe pour SAS
        if reco in ["TAVI", "SAVR", "Intervention recommandée"]:
            classe = "1"
        elif reco in ["Surveillance échographique", "Surveillance ou réévaluation"]:
            classe = "2a"
        else:
            classe = "Non classé"

        st.success(f"✅ Recommandation AHA (Classe {classe}) : {reco}")

    # 🔹 Insuffisance aortique (IA)
    elif type_valvulopathie == "Insuffisance aortique (IA)":
        st.write(f"• Valvulopathie : {type_valvulopathie}")
        st.write(f"• Symptômes présents : {symptomes_ia}")
        st.write(f"• FEVG < 55 % : {fevg_ia}")
        st.write(f"• DTDVG ≥ 70 mm : {dtdvg_sup70}")

        # Définir la recommandation AHA
        if symptomes_ia == "Oui":
            reco = "Intervention recommandée"
        elif fevg_ia == "Oui" or dtdvg_sup70 == "Oui":
            reco = "Intervention recommandée"
        else:
            reco = "Surveillance échographique"

        # Classe de recommandation
        if reco == "Intervention recommandée":
            classe = "1"
        elif reco == "Surveillance échographique":
            classe = "2a"
        else:
            classe = "Non classé"

        st.success(f"✅ Recommandation AHA (Classe {classe}) : {reco}")

    # 🔹 Insuffisance mitrale (IM)
    elif type_valvulopathie == "Insuffisance mitrale (IM)":
        st.markdown("#### Données cliniques – Insuffisance mitrale (IM)")

        st.write(f"• Valvulopathie : {type_valvulopathie}")
        st.write(f"• Symptômes présents : {symptomes_im}")
        st.write(f"• FEVG < 60 % : {fevg60}")

        if symptomes_im == "Oui" or (symptomes_im == "Non" and fevg60 == "Oui"):
            reco = "Chirurgie recommandée"
            classe = "1"
        else:
            reco = "Surveillance échographique"
            classe = "2a"

        st.success(f"✅ Recommandation AHA (Classe {classe}) : {reco}")

    # 🔹 Sténose mitrale (SM)
    elif type_valvulopathie == "Sténose mitrale (SM)":
        st.markdown("#### Données cliniques – Sténose mitrale (SM)")

        st.write(f"• Valvulopathie : {type_valvulopathie}")
        st.write(f"• Symptômes présents : {symptomes_sm}")

        if symptomes_sm == "Oui":
            reco = "Intervention recommandée"
            classe = "1"
        else:
            reco = "Surveillance échographique"
            classe = "2a"

        st.success(f"✅ Recommandation AHA (Classe {classe}) : {reco}")



# 6. PDF
if st.button("📄 Générer un rapport PDF"):
    try:
        # Détermination de la recommandation principale et de sa classe
        if sas_confirmee == "Non":
            reco = "Surveillance ou réévaluation"
            classe = "2b"
        elif symptomes_sas == "Non":
            reco = "Surveillance régulière"
            classe = "2a"
        elif risque == "Oui" or age >= 80:
            reco = "TAVI"
            classe = "1"
        else:
            reco = "SAVR"
            classe = "1"

        # Détermination de la recommandation pour SAS asymptomatique
        if symptomes_sas == "Non":
            if fegv == "Oui" or gradient == "Oui" or vmax_aha == "Oui":
                reco_asympto = "Intervention recommandée"
                classe_asympto = "1"
            else:
                reco_asympto = "Surveillance échographique"
                classe_asympto = "2a"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=safe_text("Rapport médical - Sténose Aortique Sévère"), ln=True, align="C")
        pdf.line(10, 20, 200, 20)

        pdf.cell(200, 10, txt=safe_text(f"Date : {datetime.date.today()}"), ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=safe_text("Données cliniques :"), ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=safe_text(f"- SAS confirmée : {sas_confirmee}"), ln=True)
        pdf.cell(200, 10, txt=safe_text(f"- Symptômes présents : {symptomes_sas}"), ln=True)
        pdf.cell(200, 10, txt=safe_text(f"- Risque chirurgical élevé : {risque}"), ln=True)
        pdf.cell(200, 10, txt=safe_text(f"- Âge du patient : {age} ans"), ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=safe_text(f"Recommandation AHA (Classe {classe}) : {reco}"), ln=True)

        if symptomes_sas == "Non":
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=safe_text("Décision SAS asymptomatique :"), ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=safe_text(f"- {reco_asympto} (Classe {classe_asympto})"), ln=True)

        pdf_text = pdf.output(dest='S').encode('latin-1', 'replace')
        with open("rapport_sas.pdf", "wb") as f:
            f.write(pdf_text)

        st.success("✅ Rapport PDF généré avec succès !")

        with open("rapport_sas.pdf", "rb") as file:
            st.download_button(
                label="📥 Télécharger le rapport PDF",
                data=file,
                file_name="rapport_sas.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du PDF : {e}")
