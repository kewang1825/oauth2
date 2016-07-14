/*
* Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
* See LICENSE in the project root for license information.
*/

import UIKit

/**
 SendMailViewController is responsible for sending email using the mywebapp (which talks to Microsoft Graph).
 Recipient address is pre-filled with the signed-in user's email address, and it can
 be modified.
 
 */
class SendMailViewController : UIViewController {
    // MARK: Constants, Outlets, and Properties
    // Outlets
    @IBOutlet var headerLabel: UILabel!
    @IBOutlet var emailTextField: UITextField!
    @IBOutlet var sendMailButton: UIButton!
    @IBOutlet var statusTextView: UITextView!
    @IBOutlet var activityIndicator: UIActivityIndicatorView!

    // Constants
    let successString = "Check your Inbox, you have a new message."
    let failureString = "The email couldn't be sent. Check the log for errors."

    // Properties
    var userEmailAddress: String!
    
    // MARK: ViewController methods
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        self.navigationItem.hidesBackButton = true
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.emailTextField.text = self.userEmailAddress
        
        let idx = self.userEmailAddress.characters.indexOf("@")
        self.headerLabel.text = "Hi, \(self.userEmailAddress.substringToIndex(idx!) )"
        
    }
    
    // MARK: IBActions
    @IBAction func sendMail(sender: AnyObject) {
        // Fetch content from file
        updateUI(showActivityIndicator: true, statusText: "Sending")
        self.userEmailAddress = self.emailTextField.text;
        
        let request = NSMutableURLRequest(URL: NSURL(string: "\(AuthenticationConstants.SendUri)/\(self.userEmailAddress)")!)
        request.HTTPMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json, text/plain, */*", forHTTPHeaderField: "Accept")
        
        request.setValue("Bearer \(AuthenticationManager.sharedInstance!.accessToken!)", forHTTPHeaderField: "Authorization")
        
        let task = NSURLSession.sharedSession().dataTaskWithRequest(request, completionHandler:
            {
                (data, response, error) -> Void in
                
                if let _ = error {
                    print(error)
                    self.updateUI(showActivityIndicator: false, statusText: self.failureString)
                    return
                }
                
                let statusCode = (response as! NSHTTPURLResponse).statusCode
                
                if statusCode == 202 {
                    self.updateUI(showActivityIndicator: false, statusText: self.successString)
                }
                else {
                    print("response: \(response)")
                    print(String(data: data!, encoding: NSUTF8StringEncoding))
                    self.updateUI(showActivityIndicator: false, statusText: self.failureString)
                }
        })
        
        task.resume()
        
    }
    
    @IBAction func disconnect(sender: AnyObject) {
        AuthenticationManager.sharedInstance!.clearCredentials()
        self.navigationController?.popViewControllerAnimated(true)
    }
    
    func updateUI(showActivityIndicator showActivityIndicator: Bool,
        statusText: String? = nil) {
            if showActivityIndicator {
                dispatch_async(dispatch_get_main_queue(), { () -> Void in
                    self.sendMailButton.enabled = false
                    self.activityIndicator.startAnimating()
                })
            }
            else {
                dispatch_async(dispatch_get_main_queue(), { () -> Void in
                    self.sendMailButton.enabled = true
                    self.activityIndicator.stopAnimating()
                })
            }
            if let _ = statusText {
                dispatch_async(dispatch_get_main_queue(), { () -> Void in
                    self.statusTextView.text = statusText
                })
            }
    }
}
