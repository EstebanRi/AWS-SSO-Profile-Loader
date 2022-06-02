# AWS-SSO-Profile-Loader

## Usage
<br/>

### Create profiles and update credentials
<br/>

Use `awsupdatecredentials` to create and load the profiles available for the current AWS account.

```sh
awsupdatecredentials
```
+ A new browser window will open asking for Authorization
<img style="margin:1em" src="https://gist.githubusercontent.com/EstebanRi/9534bd830145cd3971ae7ba5f26c1b8d/raw/d10cd7d9722f0b0de5d6b636ed6da70d876b1ad1/01.png">

 **If the window not opens, please use the url to login manually**

 + After a successful login, press enter and the script will generate the profiles
<img style="margin:1em" src="https://gist.githubusercontent.com/EstebanRi/9534bd830145cd3971ae7ba5f26c1b8d/raw/d10cd7d9722f0b0de5d6b636ed6da70d876b1ad1/02.png">


<br/>

### Profile
<br/>

Use `awssetprofile` to select the current profile.

```sh
awssetprofile
``` 

+ The script will display a list of available profiles and ask for the desired one
<img style="margin:1em" src="https://gist.githubusercontent.com/EstebanRi/9534bd830145cd3971ae7ba5f26c1b8d/raw/d10cd7d9722f0b0de5d6b636ed6da70d876b1ad1/03.png">

