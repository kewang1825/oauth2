/*
* Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
* See LICENSE in the project root for license information.
*/

import Foundation

// You'll set your application's ClientId and RedirectURI here. These values are provided by your Microsoft Azure app
//registration. See README.MD for more details.

struct AuthenticationConstants {

    static let ClientId    = "37e80257-7a25-40e4-a546-0649aa85f972"
    static let RedirectUri = NSURL.init(string: "http://localhost:5239")
    static let Authority   = "https://login.microsoftonline.com/common"
    static let ResourceId  = "http://localhost:5000/1/9646111a-31f7-11e6-a9a7-0f220aab2a15"

}


