
## Issue: An unexpected error occurred during the `brew link` step #645
Just Run below command

1)brew doctor

2)sudo chown -R $(whoami) $(brew --prefix)/*

3)sudo install -d -o $(whoami) -g admin /usr/local/Frameworks

note the $(brew --prefix)/* ...High Sierra doesn't allow you to change permissions on /user/local directly)

Your problem will solved 100%.

Reference: https://github.com/httpie/httpie/issues/645

## Issue: pkg-config can't find openssl though openssl was installed by homebrew 
workround
export PKG_CONFIG_PATH=/usr/local/opt/openssl/lib/pkgconfig
