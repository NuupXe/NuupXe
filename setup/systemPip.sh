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

# =============================================================================
# Script Functions
# =============================================================================

pipFunctionUpgrade() {
	sudo $pipName $pipCommandUpgrade
}

pipFunctionInstall() {
	packageName=$@
	sudo $pipName $pipCommandInstall $packageName
}

# =============================================================================
# Script Main
# =============================================================================

pipFunctionInstall $packageDistribute
pipFunctionInstall $packageFeedparser
pipFunctionInstall $packagePywws
pipFunctionInstall $packageTweepy
pipFunctionInstall $packageApscheduler

# End of file
