# Project Manager an Django App (V 0.0.1)

## Objects
	- Task: Is an assignment/work/part of work to subordinates. It has following properties
		- Task type (JIRA ticket, Learning, Training, Internal Project, Others)
		- start date
		- due date
		- assigned to
		- status (Completed, Inprocess, Under review)
	- Milestone: Is an daily amount of work contributed towards completing the ticket. It has following properties
		- Task ID
		- Time spent on Task
		- comments
		- contribution (in percentage)

## Story 1:
	Admin/Superadmin (Manager)
		- Tasks
			Create, Edit and Delete Tasks.
			View a data grid Tasks

## Story 2:
	Basic User (Repotee)
		- View tasks assigned to self.
		- Create, Edit and Delete on following items for particular Task
			- Milestones
			- Contribution

## Story 3:
	Manager Dashboard
		- Aggregation of Tasks data
			- Total open Tasks
			- Total Closed Tasks
			- Critical Tasks
		- Generate Daily Milestone report aggregated to each repotee

