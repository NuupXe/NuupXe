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
export packageApscheduler=apscheduler
export packagePyserial=pyserial
export packageWolframalpha=wolframalpha
export packagePywapi=pywapi
export packageRequests=requests
export packagePygeocoder=pygeocoder
export packageDropbox=dropbox
export packageTwython=twython

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

# End of file
