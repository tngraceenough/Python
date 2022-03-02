#!/usr/bin/env bash

echo "test"

grep -riH stage .|cut -d':' -f1 | sort -t: -u -k1,1 > file.txt

for file in $(cat file.txt); do sed -i '' 's/stage/preprod/g' $file; done



#TODO 1) Rename Folders with old env - stage - in name. Look for & Change folder names. 1a) try mv command. 1b) try find command
#cloudfront - site-cdn-stage-medicalnewstoday.com
#route53.   - frontend-stage.medicalnewstoday.com
#storage    - hl-site-mnt-stage-cdn-source
# Is there a better way?

#1a

mv ~/Documents/GitHub/infrastructure-live/site/mnt/stage/_global/cloudfront/site-cdn-stage-medicalnewstoday.com ~/Documents/GitHub/infrastructure-live/site/mnt/preprod/_global/cloudfront/site-cdn-preprod.medicalnewstoday.com

mv ~/Documents/GitHub/infrastructure-live/site/mnt/stage/_global/route53/frontend-stage.medicalnewstoday.com ~/Documents/GitHub/infrastructure-live/site/mnt/preprod/_global/route53/frontend-preprod.medicalnewstoday.com

mv ~/Documents/GitHub/infrastructure-live/site/mnt/stage/us-west-2/stage/storage/hl-site-mnt-stage-cdn-source ~/Documents/GitHub/infrastructure-live/site/mnt/preprod/us-west-2/preprod/storage/hl-site-mnt-stage-cdn-source


#1b

# Using find command. Need more work on this 

# Find the directory

# find . -depth -type d -name "site-cdn-stage-medicalnewstoday.com" 

# Find the directory and move and replace the name 

###XXX. find . -depth -type d -name "site-cdn-stage-medicalnewstoday.com" -execdir mv {} directory \;



#TODO 2)Run terragrunt run-all plan
#TODO 3)Run terragrunt run-all apply
#TODO 4)Fix (and repeat plan, apply fix until no errors)
#TODO 5) backport to old env(s)
#TODO 6) dns 


```
#ERRORS TO RESOLVE
# ACMs - us-east-1 and us-west-2; teragrunt imports; dns validation;
# datadog synthetics - path
# datadog synthetics - datadog-apm.sh script error
# terraform state bucket name - multiple errors
# cmk-preprod - encryption
# alb - acms in us-west-2
# rv-bastion-host - remove key name; check bastion connection using mssh;
# s3 bucket naming and configs - multiple errors
# vars.json
# dependency(s)
# other errors
