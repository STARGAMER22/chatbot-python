"""Chatbot 2.0 - chatbot CLI avec réponses contextuelles."""

from __future__ import annotations

import re


class Chatbot2:
    """Chatbot simple avec détection d'intentions et mémoire courte."""

    def __init__(self) -> None:
        self.nom_utilisateur: str | None = None
        self.dernier_sujet: str | None = None

    def repondre(self, message: str) -> str:
        """Génère une réponse selon l'intention détectée et le contexte."""
        texte = message.strip()
        normalise = texte.lower()

        if not normalise:
            return "Tu peux m'écrire une idée, une question ou ton humeur 🙂"

        # Mémoriser le nom utilisateur: "je m'appelle ..."
        match_nom = re.search(
            r"\bje m['’]appelle\s+([a-zA-ZÀ-ÿ\- ]{2,30})",
            normalise,
        )
        if match_nom:
            nom_capture = match_nom.group(1).strip().title()
            self.nom_utilisateur = nom_capture
            self.dernier_sujet = "identite"
            return f"Enchanté {nom_capture} ! Je m'en souviendrai."

        # Salutations
        if any(mot in normalise for mot in ("bonjour", "salut", "hello", "bonsoir")):
            prefixe = f"Bonjour {self.nom_utilisateur} !" if self.nom_utilisateur else "Bonjour !"
            self.dernier_sujet = "salutation"
            return f"{prefixe} Comment se passe ta journée ?"

        # Questions factuelles simples
        if "ton nom" in normalise or "qui es-tu" in normalise:
            self.dernier_sujet = "identite"
            return "Je suis Chatbot 2.0, un assistant conversationnel Python."

        if "aide" in normalise or "que peux-tu faire" in normalise:
            self.dernier_sujet = "aide"
            return (
                "Je peux discuter, résumer ce que tu ressens, répondre à des questions simples "
                "et garder en mémoire ton prénom pendant la conversation."
            )

        # Humeur de l'utilisateur
        if any(expr in normalise for expr in ("je vais bien", "ça va bien", "ca va bien", "je suis content", "heureux")):
            self.dernier_sujet = "humeur_positive"
            return "Super nouvelle ✨ Qu'est-ce qui t'a mis de bonne humeur ?"

        if any(expr in normalise for expr in ("je vais mal", "ça va mal", "ca va mal", "triste", "stress", "fatigu")):
            self.dernier_sujet = "humeur_negative"
            return "Désolé de l'entendre. Tu veux m'expliquer ce qui te pèse en ce moment ?"

        # Suivi contextuel d'une réponse courte
        if normalise in {"oui", "non", "peut-être", "bof"}:
            if self.dernier_sujet == "humeur_negative":
                return "Merci de me le dire. Parler un peu de la cause peut déjà aider."
            if self.dernier_sujet == "humeur_positive":
                return "J'aime cette énergie ! Continue sur cette lancée 😄"
            if self.dernier_sujet == "salutation":
                return "Ravi de l'entendre. Tu veux discuter d'un sujet en particulier ?"
            return "Compris. Si tu veux, pose-moi une question plus précise."

        # Questions ouvertes
        if "?" in texte:
            self.dernier_sujet = "question"
            return (
                "Bonne question. Je n'ai pas toutes les réponses, "
                "mais je peux t'aider à clarifier le problème étape par étape."
            )

        if "merci" in normalise:
            self.dernier_sujet = "gratitude"
            return "Avec plaisir !"

        # Fallback plus conversationnel
        prenom = f" {self.nom_utilisateur}" if self.nom_utilisateur else ""
        self.dernier_sujet = "discussion"
        return (
            f"Je vois{prenom}. Si tu veux une réponse utile, donne-moi un peu plus de contexte "
            "(objectif, problème, contraintes)."
        )


def main() -> None:
    """Lance une conversation jusqu'à la sortie utilisateur."""
    bot = Chatbot2()

    print("=== Chatbot 2.0 ===")
    print("Tape 'quit', 'au revoir' ou 'bye' pour quitter.")

    while True:
        utilisateur = input("Toi : ")
        if utilisateur.lower().strip() in {"quit", "au revoir", "bye"}:
            print("Chatbot 2.0 : À bientôt 👋")
            break

        reponse = bot.repondre(utilisateur)
        print(f"Chatbot 2.0 : {reponse}")


if __name__ == "__main__":
    main()
