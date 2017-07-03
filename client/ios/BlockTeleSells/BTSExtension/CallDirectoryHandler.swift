//
//  CallDirectoryHandler.swift
//  BTSExtension
//
//  Created by Stephen Tran on 7/2/17.
//  Copyright © 2017 STEPHENTRAN. All rights reserved.
//

import Foundation
import CallKit
import DataManager
class CallDirectoryHandler: CXCallDirectoryProvider {
    var contacts: [Contact] = []
    override func beginRequest(with context: CXCallDirectoryExtensionContext) {
        context.delegate = self
        contacts = DataManager.instance.getContacts()
        do {
            try addBlockingPhoneNumbers(to: context)
        } catch {
            NSLog("Unable to add blocking phone numbers")
            let error = NSError(domain: "CallDirectoryHandler", code: 1, userInfo: nil)
            context.cancelRequest(withError: error)
            return
        }

        do {
            try addIdentificationPhoneNumbers(to: context)
        } catch {
            NSLog("Unable to add identification phone numbers")
            let error = NSError(domain: "CallDirectoryHandler", code: 2, userInfo: nil)
            context.cancelRequest(withError: error)
            return
        }

        context.completeRequest()
    }

    private func addBlockingPhoneNumbers(to context: CXCallDirectoryExtensionContext) throws {
        // Retrieve phone numbers to block from data store. For optimal performance and memory usage when there are many phone numbers,
        // consider only loading a subset of numbers at a given time and using autorelease pool(s) to release objects allocated during each batch of numbers which are loaded.
        //
        // Numbers must be provided in numerically ascending order.
        var phoneNumbers: [Int64] = []
        for contact in contacts {
            let number = Int64("84" + String(describing: Int64(contact.phoneNumber)))
            phoneNumbers.append(number!)
        }
        //let phoneNumbers: [CXCallDirectoryPhoneNumber] = [ 843654675676, 841654675676]
        for phoneNumber in phoneNumbers.sorted(by: <) {
            context.addBlockingEntry(withNextSequentialPhoneNumber: phoneNumber)
        }
    }

    private func addIdentificationPhoneNumbers(to context: CXCallDirectoryExtensionContext) throws {
        // Retrieve phone numbers to identify and their identification labels from data store. For optimal performance and memory usage when there are many phone numbers,
        // consider only loading a subset of numbers at a given time and using autorelease pool(s) to release objects allocated during each batch of numbers which are loaded.
        //
        // Numbers must be provided in numerically ascending order.
        var phoneNumbers: [Int64] = []
        var labels: [String] = []
        for contact in contacts {
            let number = Int64("84" + String(describing: Int64(contact.phoneNumber)))
            phoneNumbers.append(number!)
            labels.append(contact.firstName + " " + contact.lastName)
        }
        if(phoneNumbers.count == 0){
            phoneNumbers = [ 841654675676 ]
            labels = [ "Telemarketer2" ]
        }

        for (phoneNumber, label) in zip(phoneNumbers, labels) {
            context.addIdentificationEntry(withNextSequentialPhoneNumber: phoneNumber, label: label)
        }
    }

}

extension CallDirectoryHandler: CXCallDirectoryExtensionContextDelegate {

    func requestFailed(for extensionContext: CXCallDirectoryExtensionContext, withError error: Error) {
        // An error occurred while adding blocking or identification entries, check the NSError for details.
        // For Call Directory error codes, see the CXErrorCodeCallDirectoryManagerError enum in <CallKit/CXError.h>.
        //
        // This may be used to store the error details in a location accessible by the extension's containing app, so that the
        // app may be notified about errors which occured while loading data even if the request to load data was initiated by
        // the user in Settings instead of via the app itself.
    }

}
