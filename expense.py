# FUNCTIONS
# Export search results to text file
def export(array, total_amt):
	count = 0

	# check if file already exists
	file_exists = os.path.exists('Expense_Report.txt')
	if file_exists:
		file = open("Expense_Report.txt","a") # append to file
		for row in array:  
			count = count + 1
			if count != 1:   # dont printout headings as file already exist (i.e. not the very first entry)
				file.write("{: >20} {: >20} {: >20}".format(*row)) # append expense details to file
				file.write('\n')
	else:  # file doesnt exist (i.e. very first entry)
		file = open("Expense_Report.txt","w") # overwrite existing same name file
		for row in array:  
			file.write("{: >20} {: >20} {: >20}".format(*row)) # append expense details to file (including heading)
			file.write('\n')
	file.close()

# Search expense details by selected date
def searchbydate(array, date, special, tmp, total_amt, array_result, usr_export, count):
	# append headers to array_result
	array_result = np.append(array_result, np.array([["Date", "Description", "Amount"]]), axis=0)
	match_date = np.where(array == date) # search for date within array				
	match_index = list(zip(match_date[0], match_date[1])) # zip coordinates of date within array

	# append matches to array_result
	for coordinate in match_index: # if list is not empty
		row = (coordinate[0])  # row number of date
		expense_desc = array[row][1] # 2nd column = description
		expense_amt = array[row][2] # 3rd column = amount
		array_result = np.append(array_result, np.array([[date, expense_desc, expense_amt]]), axis=0) # store expense details into array_result
		total_amt = total_amt + float(expense_amt) # calculate total amount for each date

	# if not even 1 match is found, output "no records found"
	# if at least 1 match is found, ignore those without matches
	if len(array_result) > 1:  # array has more than 1 row (i.e. have at least 1 match)

		count = count + 1 # ensure that only the 3 headings are printed for the very first time round
		if count == 1:
			for row in array_result: # print all matching result + first row of heading
				print("{: >20} {: >20} {: >20}".format(*row))
		else:
			for row in array_result[1:]: # print all matching result but w/o first row of heading
				print("{: >20} {: >20} {: >20}".format(*row))
			 
	else: # array is empty (i.e. no matches at alL)  
		if special == 1:  # from single date. if special equals to 99, means it's called by date range search
			print("No records found.\n")
		else: # from range. possibility that only 3 result out of 7 days cannot be found. but we shuold only output 'no record found' once instead of 3 times
			tmp = tmp + 1

	# export expense report
	if usr_export == 1:  # user wants to export
		export(array_result, total_amt)

	return tmp, total_amt, array_result, count

# Search expense details by selected date range
def searchbyrange(array, daterange, tmp, total_amt, array_result, usr_export, count):
	# list out all dates within daterange list. get list of expense details for each date
	for date in daterange:
		result = searchbydate(array, date, 99, tmp, total_amt, array_result, usr_export, count) # search each day 1 by 1
		tmp = result[0]
		total_amt = result[1]
		count = result[3]

	return tmp, total_amt, array_result, count

# MAIN PROGRAM
import numpy as np
import pandas as pd
import datetime
import sys
import os.path
from datetime import date
from dateutil import parser

# Initialize variables
total_amt = 0
tmp = 0
i = 1
array = np.empty((0, 3), str)   # 2D array with 3 cols to store expenses
array_result = np.empty((0, 3), str)  # 2D array with 3 cols to store results of expense search
usr_export = 0
count = 0

while i == 1:
	print("\n====== Welcome to Expense Tracker v1.0 ======")
	print("1) Add Expense\n2) View Expense\n3) Convert Text File to CSV & Excel\n4) Exit\n==============================================")
	user_option = input("Please select your option: ")

	# Option 4: Exit program
	if user_option == "4":
		print("Thank you for using Expense Tracker. Have a nice day!\n")
		exit(1)

	# Option 3: Convert text file to excel
	if user_option == "3":
		print("Selected Option -> 3) Convert Text File to CSV & Excel")
		# user enter text file name
		read_txt_file = input("\nEnter filename (exclude .txt): ") # later: input validation

		# check if text file exists
		file_exists = os.path.exists(read_txt_file + ".txt")
		if file_exists:
			# convert text file to csv
			print("\nGenerating CSV file...")
			csv_file = read_txt_file + ".csv"
			txt_file_input = pd.read_csv (read_txt_file + ".txt")
			txt_file_input.to_csv (csv_file, index=None)
			print(csv_file, "has been created.")

			# convert csv to excel
			print("\nGenerating Excel file...")
			excel_file = read_txt_file + ".xlsx"
			df = pd.read_csv(csv_file)
			df.to_excel(excel_file, index = None, header=True) 
			print(excel_file, "has been created.")
		else:
			print("\nError: File not found.\nReturning to Main Menu ...")

	# Option 1: Add expense
	if user_option == "1":
		print("Selected Option -> 1) Add Expense")
		dd = input("\nEnter expense date (DD): ") # later: input validation
		mm = input("Enter expense date (MM): ")
		yy = input("Enter expense date (YYYY): ")		
		expense_date = dd + "/" + mm + "/" + yy

		# Append expense details into array
		expense_desc = input("Enter expense description: ")
		expense_amt = input("Enter expense amount: $")
		array = np.append(array, np.array([[expense_date, expense_desc, expense_amt]]), axis=0)

	# Option 2: View expense
	if user_option == "2":
		print("Selected Option -> 2) View Expense")
		j = 1
		while j == 1: # Sub menu for filtering of dates
			print("\n==========Filter Sub Menu==========\nSelect Filter Type: \n1) Date\n2) Date Range\n3) Exit\n===================================")
			user_option2 = input("Please select your option: ")
			if user_option2 == "1": # Search by single date
				# if file exist, remove it
				if os.path.exists("Expense_Report.txt"):
					os.remove("Expense_Report.txt")

				dd = input("\nEnter date (DD): ") # later: input validation
				mm = input("Enter date (MM): ")
				yy = input("Enter date (YYYY): ")
				date1 = dd + "/" + mm + "/" + yy

				# ask if user wants to export to excel
				export_input = input("\nDo you want to export results to text file (Y/N): ") # later: ask user for filename
				if export_input == "Y" or export_input == "y":
					usr_export = 1

				# get expense details based on selected date
				print("\nSearching for expenses incurred on ", date1, "...\n")
				result = searchbydate(array, date1, 1, tmp, total_amt, array_result, usr_export, count)
				array_result = result[2]
				total_amt = result[1]
				count = result[3]

				# display total expenses on selected date
				total_amt_2dp = "{:.2f}".format(total_amt) # format total amount to 2 decimal places
				print("Total Expenses: $", total_amt_2dp)

				if usr_export == 1:
					file = open("Expense_Report.txt","a")
					file.write("\nTotal Expenses: $")
					file.write(str(total_amt_2dp)) #print total amount in last line
					file.write("\n")
					print("\nExpense_Report.txt has been created.")
					file.close()

					# print selected date(s) into first line of text file
					file = open("Expense_Report.txt","r")
					original = file.read()
					file = open("Expense_Report.txt","w")
					file.write("Selected Date(s): " + date1 +"\n" + original)
					file.close()

				# reset all counters & array
				total_amt = 0 
				array_result = np.empty((0, 3), str) 
				usr_export = 0
				count = 0
				
			if user_option2 == "2": # Search by date range
				# if file exist, remove it
				if os.path.exists("Expense_Report.txt"):
					os.remove("Expense_Report.txt")

				print("Enter date range to proceed")

				dd_from = input("\nEnter From date (DD): ") # later: validation to ensure To date is later
				mm_from = input("Enter From date (MM): ")
				yy_from = input("Enter From date (YYYY): ")
				dd_to = input("\nEnter To date (DD): ")
				mm_to = input("Enter To date (MM): ")
				yy_to = input("Enter To date (YYYY): ")

				# ask if user wants to export to excel
				export_input = input("\nDo you want to export results to text file (Y/N): ") # later: ask user for filename
				if export_input == "Y" or export_input == "y":
					usr_export = 1

				# concentate date for print purpose
				date_from = dd_from + "/" + mm_from + "/" + yy_from
				date_to = dd_to + "/" + mm_to + "/" + yy_to

				print("\nSearching for expenses incurred from ", date_from, " to ", date_to, "...\n")
				date_print = "Selected Date(s): " + date_from + " - " + date_to

				# convert from str to int
				dd_from = int(dd_from)
				mm_from = int(mm_from)
				yy_from = int(yy_from)
				dd_to = int(dd_to)
				mm_to = int(mm_to)
				yy_to = int(yy_to)				

				# calculate number of days inclusive of start & end
				d1 = date(yy_to,mm_to,dd_to)
				d2 = date(yy_from, mm_from, dd_from)
				days_range = abs(d2-d1).days + 1 
				
				# get list of eligible dates
				date_from = datetime.date(yy_from,mm_from,dd_from)
				daterange = []
				for day in range(days_range):
					date1 = (date_from + datetime.timedelta(days = day)).isoformat()
					date1 = parser.parse(date1) # convert string to datetime type
					date1 = date1.strftime("%d/%m/%Y") # convert from yyyy-mm-dd to dd-mm-yyyy
					daterange.append(date1)			

				# get list of expense details based on selected date range
				result = searchbyrange(array, daterange, tmp, total_amt, array_result, usr_export, count)
				tmp = result[0]
				total_amt = result[1]
				if days_range == tmp:  # e.g. 7 out of 7 dates not found. so will only output failed message once
					print("No records found.\n")
				
				array_result = result[2]
				count = result[3]

				# display total expenses within selected date range
				total_amt_2dp = "{:.2f}".format(total_amt) # format total amount to 2 decimal places
				print("Total Expenses: $", total_amt_2dp)

				if usr_export == 1:
					file = open("Expense_Report.txt","a")
					file.write("\nTotal Expenses: $")
					file.write(str(total_amt_2dp)) #print total amount in last line
					file.write("\n")
					print("\nExpense_Report.txt has been created.")
					file.close()

					# print selected date(s) into first line of text file
					file = open("Expense_Report.txt","r")
					original = file.read()
					file = open("Expense_Report.txt","w")
					file.write(date_print + "\n" + original)
					file.close()

				# reset counters & array
				tmp = 0
				total_amt = 0
				array_result = np.empty((0, 3), str)
				usr_export = 0
				count = 0

			if user_option2 == "3": # Exit sub menu
				print("Returning to Main Menu ...")
				break
