#!/bin/sh

# =============================================================================
# Scripts Variables General
# =============================================================================

export pipName=pip
export pipCommandInstall=install
export pipCommandUpgrade=--upgrade

# =============================================================================
# Scripts Variables Local
# =============================================================================

export packageDistribute=distribute
export packageFeedparser=feedparser
export packagePywws=pywws
export packageTweepy=tweepy
export packageApscheduler=apscheduler==2.1.0
export packagePyserial=pyserial
export packageWolframalpha=wolframalpha
export packagePywapi=pywapi
export packageRequests=requests==2.6.0
export packagePygeocoder=pygeocoder
export packageDropbox=dropbox
export packageTwython=twython
export packageYowsup2=yowsup2
export packagePsutil=psutil
export packageGitPython=gitpython
export packageTropo=tropo-webapi-python
export packagePySSTV=pySSTV
export packageXmlToDict=xmltodict
export packageNumPy=numpy
export packageSpeechRecognition=SpeechRecognition
export packageTelepot=telepot

# =============================================================================
# Script Functions
# =============================================================================

pipFunctionUpgrade() {
	$pipName $pipCommandUpgrade
}

pipFunctionInstall() {
	packageName=$@
	$pipName $pipCommandInstall $packageName
}

# =============================================================================
# Script Main
# =============================================================================

$pipName install -U pip

pipFunctionInstall $packageDistribute
pipFunctionInstall $packageFeedparser
pipFunctionInstall $packagePywws
pipFunctionInstall $packageTweepy
pipFunctionInstall $packageApscheduler
pipFunctionInstall $packagePyserial
pipFunctionInstall $packageWolframalpha
$pipName install --allow-all-external $packagePywapi --allow-unverified $packagePywapi
pipFunctionInstall $packageRequests
pipFunctionInstall $packagePygeocoder
pipFunctionInstall $packageDropbox
pipFunctionInstall $packageTwython
#pipFunctionInstall $packageYowsup2
pipFunctionInstall $packagePsutil
pipFunctionInstall $packageGitPython
pipFunctionInstall $packageTropo
pipFunctionInstall $packagePySSTV
pipFunctionInstall $packageXmlToDict
pipFunctionInstall $packageNumPy
pipFunctionInstall $packageSpeechRecognition
pipFunctionInstall $packageTelepot

# End of file
