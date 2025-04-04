#!/bin/bash

# Couleurs pour la sortie console
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Configuration de l'environnement virtuel pour Alien Invader...${NC}"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Python3 n'est pas installé. Veuillez installer Python 3.6 ou supérieur."
    exit 1
fi

# Création de l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv .venv

# Vérifier si la création a réussi
if [ ! -d ".venv" ]; then
    echo "Erreur: Impossible de créer l'environnement virtuel."
    exit 1
fi

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier si l'activation a réussi
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Erreur: Impossible d'activer l'environnement virtuel."
    exit 1
fi

# Mise à jour de pip
echo "Mise à jour de pip..."
pip install --upgrade pip

# Installation des dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

echo -e "${GREEN}Configuration terminée avec succès!${NC}"
echo -e "${BLUE}Pour activer l'environnement ultérieurement, utilisez:${NC}"
echo -e "source .venv/bin/activate"
echo ""
echo -e "${BLUE}Pour lancer le jeu:${NC}"
echo -e "python main.py"

# Informations sur l'environnement
echo ""
echo -e "${BLUE}Informations sur l'environnement:${NC}"
python --version
pip --version
pip list

# Laisser l'environnement activé pour l'utilisateur
echo ""
echo -e "${GREEN}L'environnement virtuel est maintenant activé et prêt à l'emploi.${NC}"

# Demande si l'utilisateur souhaite activé l'environnement virtuel
read -p "Souhaitez-vous activer l'environnement virtuel maintenant ? (o/n) " choice
if [[ $choice == "o" || $choice == "O" ]]; then
    echo -e "${GREEN}L'environnement virtuel est maintenant activé.${NC}"
    source .venv/bin/activate
else
    echo -e "${GREEN}Vous pouvez activer l'environnement virtuel plus tard en exécutant :${NC}"
    echo -e "source .venv/bin/activate"
fi