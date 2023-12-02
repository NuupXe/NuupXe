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

export packageFestival="festival festlex-cmu festlex-poslex festvox-kallpc16k festvox-ellpc11k"
export packagePyPi="python3-pip"
export packagePygame="python3-pygame"
export packageMpg123="mpg123"
export packageSeveral="ffmpeg flac"
export packageText2Speech="festival espeak"
export packageCurl="curl"
export packageFswebcam="fswebcam"
export packagePythonDev="python3-dev"
export packageFlac="flac"
export packagePythonPil="python-pil"
export packageLibAsound2Dev="libasound2-dev"
export packageLibJpegDev="libjpeg-dev"
export packageLibFfi="libffi-dev"
export packageLibSsl="libssl-dev"
export packageFlac="flac"
export packagePythonFeedparser="python3-feedparser"
export packagePythonPyAudio="python3-pyaudio"
export packagePythonPsutil="python3-psutil"
export packagePythonPyserial="python3-pyserial"
export packagePythonTweepy="python3-tweepy"
export packagePythonTwython="python3-twython"
export packageLibSoxDev="libsox-dev"
export packageImageMagick="imagemagick"
export packagePortaudio19dev="portaudio19-dev"

# =============================================================================
# Script Functions
# =============================================================================

aptgetFunctionUpdate() {
	$aptgetName $aptgetCommandUpdate
}

aptgetFunctionInstall() {
	packageName=$@
	$aptgetName $aptgetCommandInstall $packageName
}

# =============================================================================
# Script Main
# =============================================================================

aptgetFunctionUpdate

aptgetFunctionInstall $packageGit

#aptgetFunctionInstall $packageKernelPackage
#aptgetFunctionInstall $packageLibNCurses5
#aptgetFunctionInstall $packageLibNCursesDev

#aptgetFunctionInstall $packageAx25Tools
#aptgetFunctionInstall $packageAx25Xtools
#aptgetFunctionInstall $packageAx25Apps
#aptgetFunctionInstall $packageLibAx25Dev

aptgetFunctionInstall $packageFestival
aptgetFunctionInstall $packagePyPi
aptgetFunctionInstall $packagePygame
aptgetFunctionInstall $packageMpg123
aptgetFunctionInstall $packageSeveral
aptgetFunctionInstall $packageText2Speech
aptgetFunctionInstall $packageCurl
aptgetFunctionInstall $packageFswebcam
aptgetFunctionInstall $packagePythonDev
aptgetFunctionInstall $packagePythonPywapi
aptgetFunctionInstall $packageFlac
aptgetFunctionInstall $packagePythonImage
aptgetFunctionInstall $packageLibAsound2Dev
aptgetFunctionInstall $packageLibJpegDev
aptgetFunctionInstall $packagePythonImaging
aptgetFunctionInstall $packageGnuRadio
aptgetFunctionInstall $packageSdr
aptgetFunctionInstall $packageLibFfi
aptgetFunctionInstall $packageLibSsl
aptgetFunctionInstall $packageFlac
aptgetFunctionInstall $packagePythonFeedparser
aptgetFunctionInstall $packagePythonPyAudio
aptgetFunctionInstall $packagePythonPyserial
aptgetFunctionInstall $packagePythonTweepy
aptgetFunctionInstall $packagePythonTwython
aptgetFunctionInstall $packageLibSoxDev
aptgetFunctionInstall $packageImageMagick
aptgetFunctionInstall $packagePortaudio19dev

# End of file
