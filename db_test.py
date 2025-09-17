
file_structure = {
  "phases": [
    {
      "name": "Phase 1: Core Setup & State Management",
      "description": "Establish the foundational elements of the application, including theme, routing, global state management, and mock data.",
      "batches": [
        {
          "name": "Batch 1: Configuration",
          "description": "Update base files for theme, fonts, and routing structure.",
          "files": [
            "index.html",
            "src/theme.js",
            "src/router.jsx"
          ]
        },
        {
          "name": "Batch 2: Global State",
          "description": "Set up the Redux store and slices for managing tasks and UI state.",
          "files": [
            "src/store/store.js",
            "src/store/slices/tasksSlice.js",
            "src/store/slices/uiSlice.js"
          ]
        },
        {
          "name": "Batch 3: Data and Validation",
          "description": "Create mock data for initial state and Zod schema for form validation.",
          "files": [
            "src/services/mockData.js",
            "src/schemas/taskSchema.js"
          ]
        }
      ]
    },
    {
      "name": "Phase 2: Layout & Shared Components",
      "description": "Build the main application layout and shared navigation components.",
      "batches": [
        {
          "name": "Batch 4: Application Shell",
          "description": "Create the main layout including the top app bar and bottom navigation, and integrate them in the main App component.",
          "files": [
            "src/layouts/MainLayout.jsx",
            "src/components/shared/TopAppBar.jsx",
            "src/components/shared/BottomNavBar.jsx",
            "src/App.jsx"
          ]
        }
      ]
    },
    {
      "name": "Phase 3: Feature Pages & Components",
      "description": "Develop the primary pages of the application and their specific components.",
      "batches": [
        {
          "name": "Batch 5: Dashboard",
          "description": "Build the main dashboard page and its UI sections.",
          "files": [
            "src/pages/DashboardPage.jsx",
            "src/components/dashboard/UpcomingDeadlines.jsx",
            "src/components/dashboard/BalanceOverview.jsx",
            "src/components/dashboard/QuickActions.jsx"
          ]
        },
        {
          "name": "Batch 6: Schedule",
          "description": "Build the schedule page for viewing tasks on a timeline.",
          "files": [
            "src/pages/SchedulePage.jsx",
            "src/components/schedule/TaskItem.jsx"
          ]
        },
        {
          "name": "Batch 7: Progress Tracking",
          "description": "Build the progress tracking page, its components, and related detail screens.",
          "files": [
            "src/pages/ProgressPage.jsx",
            "src/components/progress/BalanceWheel.jsx",
            "src/components/progress/StudyStreakCalendar.jsx",
            "src/pages/BalanceDetailPage.jsx",
            "src/pages/StreakHistoryPage.jsx"
          ]
        },
        {
          "name": "Batch 8: Prioritization",
          "description": "Build the prioritization page with its interactive matrix.",
          "files": [
            "src/pages/PrioritizationPage.jsx",
            "src/components/prioritization/PriorityMatrix.jsx"
          ]
        }
      ]
    },
    {
      "name": "Phase 4: Modals and Interactions",
      "description": "Create the modal dialogs for adding/editing tasks and filtering views.",
      "batches": [
        {
          "name": "Batch 9: Core Modals",
          "description": "Implement the modals for adding a new task, viewing task details, and filtering options.",
          "files": [
            "src/components/modals/AddTaskModal.jsx",
            "src/components/modals/TaskDetailModal.jsx",
            "src/components/modals/FilterViewOptionsModal.jsx"
          ]
        }
      ]
    }
  ]
}

phases = file_structure["phases"]

for phase in phases:
    batches_in_phase = phase["batches"]
    for batch in batches_in_phase:
        print(f"  - Generating files for {batch['name']}: {batch['files']}")