#!/bin/bash

show_welcome() {
    clear  # Clear the screen for a clean look

    echo ""
    sleep 0.2
    echo " _   _      _ _          ____    _    __  __ ____           _ "
    sleep 0.2
    echo "| | | | ___| | | ___    / ___|  / \  |  \/  |  _ \ ___ _ __| |"
    sleep 0.2
    echo "| |_| |/ _ \ | |/ _ \  | |     / _ \ | |\/| | |_) / _ \ '__| |"
    sleep 0.2
    echo "|  _  |  __/ | | (_) | | |___ / ___ \| |  | |  __/  __/ |  |_|"
    sleep 0.2
    echo "|_| |_|\___|_|_|\___/   \____/_/   \_\_|  |_|_|   \___|_|  (_)"
    sleep 0.5

echo ""
echo "🌲🏕️    WELCOME TO CAMP SETUP! 🏕️  🌲"
echo "===================================================="
echo ""
echo "   🏕️    Configuring Databases & Conda Environments"
echo "       for CAMP short-read assembly"
echo ""
echo "   🔥 Let's get everything set up properly!"
echo ""
echo "===================================================="
echo ""

}

show_welcome

# Set work_dir
DEFAULT_PATH=$PWD
read -p "Enter the working directory (Press Enter for default: $DEFAULT_PATH): " USER_WORK_DIR
SR_ASSEMBLY_WORK_DIR="$(realpath "${USER_WORK_DIR:-$PWD}")"
echo "Working directory set to: $SR_ASSEMBLY_WORK_DIR"
#echo "export ${SR_ASSEMBLY_WORK_DIR} >> ~/.bashrc" 

# Install conda envs: assemblers, quast
cd $DEFAULT_PATH
DEFAULT_CONDA_ENV_DIR=$(conda info --base)/envs

# Function to check and install conda environments
check_and_install_env() {
    ENV_NAME=$1
    CONFIG_PATH=$2

    if conda env list | grep -q "$DEFAULT_CONDA_ENV_DIR/$ENV_NAME"; then
        echo "✅ Conda environment $ENV_NAME already exists."
    else
        echo "Installing Conda environment $ENV_NAME from $CONFIG_PATH..."
        CONDA_CHANNEL_PRIORITY=flexible conda env create -f "$CONFIG_PATH" || { echo "❌ Failed to install $ENV_NAME."; return; }
    fi
}

# Check and install environments
check_and_install_env "assemblers" "configs/conda/assemblers.yaml"
check_and_install_env "quast" "configs/conda/quast.yaml"
check_and_install_env "dataviz" "configs/conda/dataviz.yaml"

# Generate parameters.yaml
SCRIPT_DIR=$(pwd)
EXT_PATH="$SR_ASSEMBLY_WORK_DIR/workflow/ext"
PARAMS_FILE="test_data/parameters.yaml"

# Remove existing parameters.yaml if present
[ -f "$PARAMS_FILE" ] && rm "$PARAMS_FILE"
# Create new parameters.yaml file
echo "#'''Parameters config.'''#

# --- general --- #

ext: '$EXT_PATH'
conda_prefix: '$DEFAULT_CONDA_ENV_DIR'
# Choose either 'megahit', 'metaspades', or both
assembler:  'metaspades,megahit'
# The default is 'meta' (metagenomics DNA) but one of 'rna' (RNA-Seq), 'metaviral' (viral DNA in a metagenomic context), or 'metaplasmid' (plasmid DNA in a metagenomic context) can also be selected
option:     'meta'" > "$PARAMS_FILE"

echo "✅ parameters.yaml file created successfully in test_data/"

# Generate configs/parameters.yaml
PARAMS_FILE="configs/parameters.yaml"
# Remove existing parameters.yaml if present
[ -f "$PARAMS_FILE" ] && rm "$PARAMS_FILE"
# Create new parameters.yaml file
echo "#'''Parameters config.'''#

# --- general --- #
ext: '$EXT_PATH'
conda_prefix: '$DEFAULT_CONDA_ENV_DIR'

# Choose either 'megahit', 'metaspades', or both
assembler:  'metaspades,megahit'
# The default is 'meta' (metagenomics DNA) but one of 'rna' (RNA-Seq), 'metaviral' (viral DNA in a metagenomic context), or 'metaplasmid' (plasmid DNA in a metagenomic context) can also be selected
option:     'meta'" > "$PARAMS_FILE"

# Modify test_data/samples.csv
sed -i.bak "s|/path/to/camp_short-read-assembly|$DEFAULT_PATH|g" test_data/samples.csv

echo "✅ parameters.yaml file created successfully in configs/"

echo "🎯 Setup complete! You can now <F5>test the workflow using \`python workflow/short-read-assembly.py test\`"
