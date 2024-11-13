
        [Setup]
        AppName=WatchdogHandler
        AppVersion=1.0
        DefaultDirName=C:\Program Files\WatchdogHandler
        DefaultGroupName=WatchdogHandler
        OutputDir=c:\Assignment\FYP\output
        OutputBaseFilename=WatchdogHandlerInstaller
        Compression=lzma
        SolidCompression=yes

        [Files]
        Source: "C:\Assignment\FYP\Children\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

        [Icons]
        Name: "{group}\WatchdogHandler"; Filename: "{app}\watchdogHandler.exe"

        [INI]
        Filename: "{app}\config.ini"; Section: "Security"; Key: "PublicKey"; String: "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4QJVZgEq/V4oATXb/Cx0\nHlM5xyiUMT9otXpd5QXhdCFQYPKp9MSrq+ufLW4JngGt8UecQG9kLTYwwOEeyWMX\n/IOatsTG3jxrLmSMemR0y148ce3Z3vGWf2fFQN94CPimDHXoLiOBxM+3TZmYb7Lw\nFhXXEtgyXxtPyZXc/XMxBi+a+gYUneQo97NiPKLNsIWXoxZVNDmB6+zGplJpsULS\nXKMIeoJ4giMYWmaE7fUH3gBD2pA5VdzJ7zbHGCuQdONpxCboD6WTDLmU4az+4dyM\nTbgCKfBEIwnM8akG6oz4Bm0Y/eZfNPb4hX9yntjyOzZEWKfWnaceJ2CEMd+nFAhy\n+QIDAQAB\n-----END PUBLIC KEY-----"
        