#!/bin/sh

# =============================================================================
# Scripts Variables General
# =============================================================================

export aptgetName=apt-get
export aptgetCommandUpdate=update
export aptgetCommandInstall="install --yes"

# =============================================================================
# Scripts Variables Local
# =============================================================================

export packageGit=git

export packageKernelPackage=kernel-package
export packageLibNCurses5=libncurses5
export packageLibNCursesDev=libncurses-dev

export packageAx25Tools=ax25-tools
export packageAx25Xtools=ax25-xtools
export packageAx25Apps=ax25-apps
export packageLibAx25Dev=libax25-dev

export packageFestival="festival festlex-cmu festlex-poslex festvox-kallpc16k libestools1.2 festvox-ellpc11k"

export packagePyPi="python-pip"

export packagePygame="python-pygame"

# =============================================================================
# Script Functions
# =============================================================================

aptgetFunctionUpdate() {
	sudo $aptgetName $aptgetCommandUpdate
}

aptgetFunctionInstall() {
	packageName=$@
	sudo $aptgetName $aptgetCommandInstall $packageName
}

# =============================================================================
# Script Main
# =============================================================================

aptgetFunctionUpdate

aptgetFunctionInstall $packageGit

aptgetFunctionInstall $packageKernelPackage
aptgetFunctionInstall $packageLibNCurses5
aptgetFunctionInstall $packageLibNCursesDev

aptgetFunctionInstall $packageAx25Tools
aptgetFunctionInstall $packageAx25Xtools
aptgetFunctionInstall $packageAx25Apps
aptgetFunctionInstall $packageLibAx25Dev

aptgetFunctionInstall $packageFestival

aptgetFunctionInstall $packagePyPi

aptgetFunctionInstall $packagePygame

# End of file
