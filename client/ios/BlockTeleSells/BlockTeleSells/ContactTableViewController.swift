//
//  ContactListTableViewController.swift
//  CallBlock
//
//  Created by Stephen Tran on 6/30/17.
//  Copyright © 2017 STEPHENTRAN. All rights reserved.
//

import UIKit
import os.log
import DataManager
class ContactTableViewController: UITableViewController {
    var contacts = [Contact]()
    override func viewDidLoad() {
        super.viewDidLoad()
        navigationItem.leftBarButtonItem = editButtonItem
        loadContacts();
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
         //self.navigationItem.rightBarButtonItem = self.editButtonItem()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return contacts.count
    }

    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "ContactTableViewCell"
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? ContactTableViewCell else {
        
            fatalError("The dequeued cell is not an instance of MealTableViewCell.")
        }
        let contact = contacts[indexPath.row]
        cell.contactPhoneNumber.text = contact.phoneNumber
        cell.contactDescription.text = contact.description

        return cell
    }
    

    
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
 

    
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            DataManager.instance.deleteContact(cid: contacts[indexPath.row].id!)
            contacts.remove(at: indexPath.row)
            tableView.deleteRows(at: [indexPath], with: .fade)
            
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
 

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        super.prepare(for: segue, sender: sender)
        switch(segue.identifier ?? "") {
            case "AddItem":
                os_log("Adding a new meal.", log: OSLog.default, type: .debug)
            case "ShowDetail":
                guard let contactDetailViewController = segue.destination as? ContactViewController else {
                    fatalError("Unexpected destination: \(segue.destination)")
                }
                guard let selectedMealCell = sender as? ContactTableViewCell else {
                    fatalError("Unexpected sender: \(sender)")
                }
 
                guard let indexPath = tableView.indexPath(for: selectedMealCell) else {
                    fatalError("The selected cell is not being displayed by the table")
                }
 
                let selectedContact = contacts[indexPath.row]
                contactDetailViewController.contact = selectedContact
            default:
                fatalError("Unexpected Segue Identifier; \(segue.identifier)")

        }

    }
 

    //MARK: Actions
    @IBAction func unwindToContactList(sender: UIStoryboardSegue) {
        if let sourceViewController = sender.source as? ContactViewController, let contact = sourceViewController.contact {
        
            if let selectedIndexPath = tableView.indexPathForSelectedRow {
                // Update an existing contact.
                contacts[selectedIndexPath.row] = contact
                tableView.reloadRows(at: [selectedIndexPath], with: .none)
            }
            else {
                // Add a new contact.
                let newIndexPath = IndexPath(row: contacts.count, section: 0)
                contacts.append(contact)
                tableView.insertRows(at: [newIndexPath], with: .automatic)
            }
            
        }
    }
    //MARK: private
    private func loadContacts() {
        let phones = DataManager.instance.getPhoneNumbers()
        for (number, fullname) in phones {
            NSLog(number.description)
            NSLog(fullname)
        }
        contacts = DataManager.instance.getContacts()
    }

}
