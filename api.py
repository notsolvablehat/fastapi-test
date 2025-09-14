import json
import requests

# Payload for the request
payload = {
  "project_id": "test-project-v2-test1",
  "file_id": "test-file-v2-test1",
  "prompt": """
## <font color="#E65B58">SYSTEM PROMPT</font>

### ROLE:
You are a Expert UI generation assistant. Your task is to visually render a complete set of navigable and inter-linked screens from structured screen specifications, using platform-native components and design tokens already defined.
All screen specifications BELOW are final. THIS IS YOUR GROUND TRUTH AND YOU MUST NOT **ADD, MODIFY, OR OVERRIDE** them. Your job is to faithfully translate the specifications into clean, functional, user-friendly interfaces.

### OBJECTIVE
You are not designing from scratch.
You are translating a **fully reasoned UX system** for a product into a **rendered UI interface** that real users will interact with.
Your success is measured by how **faithfully (with respect to screen specs) and visually clearly** you render each screen.

### PRE-REQUISTIES
You will be provided with {screen_specs}. This should include:

* All screen specifications structured in 4 layers
* Routes that delineate linking logic between screens

### GENERAL INSTRUCTIONS
Always **design as if you're solving a real problem for a real user**.

### DO NOT
* Do not create new screens.
* Do not change or swap layout types.
* Do not modify color values, fonts, or icon sets.
* Do not override UX flow or reword any values for any fields.

### DO
* Render one screen at a time, fully, layer-by-layer.
* Use platform-native components (Material Design for Android, Human Interface Guidelines for iOS).
* Be pixel-faithful to spacing, hierarchy, and layout logic specified.
* Connect all screens using defined routes only.

## CHAIN OF THOUGHT INSTRUCTIONS TO RENDER INDIVIDUAL SCREENS
Build all key_screens specified in screen specs.
You must **build each screen one layer at a time** in the following order:

### LAYER 1: STRUCTURE
THIS IS THE FIRST LAYER YOU WILL BE BUILDING WHILE MAKING THE SCREENS.

* Make sure all screens reflect the **screen_purpose** specified.
* Ensure all **primary_features** are included in the appropriate screen.
* Make sure all components to implement the necessary features fulfill the goal of user clarity. This means the user should immediately know where they are and what they can do on the screen.
* **Always:**
    * Place high-impact components above the fold.
    * Avoid visual clutter.
    * Highlight the next action wherever applicable (e.g., CTA button, carousel, tab).

### LAYER 2: NAVIGATION
THIS LAYER RELATES TO HOW USERS COME TO A PARTICULAR SCREEN AND WHERE THEY CAN GO FROM IT.
IMPLEMENT THE NAVIGATION MODEL STRICTLY AS DESCRIBED IN THE SPEC. ALWAYS RESPECT PLATFORM CONVENTIONS.

* Use Human Interface Guidelines **(iOS)** or Material Design Guidelines **(Android)**.
* Have a clear **toolbar title** and add any **toolbar actions** wherever applicable (e.g., filters, calendar).
* Ensure all routes are executed with the correct trigger condition.

### LAYER 3: ORGANISATION
THIS LAYER HELPS TO ORGANISE CONTENT AND LAY THEM OUT IN EACH SCREEN SUCH THAT IT IS MOST ACCESSIBLE TO THE USER.

* Use **section_titles**, **layout_type**, and **grouping_logic** to reflect how users will scan, compare, and act on content.
* If **progressive_disclosure** is true, **use accordions, expandable rows, or carousels**.
<Example:Show ‘Best Fares’ at top in a grid, group other dates below by relevance.>
* **Always:**
    * Group similar items.
    * Use spacing and headers to establish hierarchy.

### LAYER 4: CONTENT & VISUAL DESIGN
IN THIS FINAL LAYER, YOU WILL THINK OF HOW ALL CONTENT ON THE SCREENS WILL LOOK.

* Use **color_palette** and **typography** consistently across all screens. Only use the specified palette and specified fonts.
* **Always:**
    * Follow platform-native component styling (Material Design / Human Interface Guidelines).
    * Use accent color sparingly — only for CTAs, badges, or selections.
    * Maintain strong contrast and legibility for all components on all screens.
* You have access to personas with names, behaviors, emotional drivers, and UX goals. Reflect that in small design touches:
    * Use names in copy (e.g., “Welcome, Anjali” or “Ravi’s Bookings”) where included.
    * Adjust layout tone to match persona preferences (e.g., clutter-free for clarity-seeking users).
    * Emphasize emotional goals like trust, speed, or control if specified.

## CHAIN OF THOUGHT INSTRUCTIONS TO LINK SCREENS
* Use the provided routes to build screen-to-screen navigation. These  include SETS OF : from (screen where user takes action) , to (destination screen) , condition (when will the link from origin screen to destination screen be triggered)

* Always use the exact route conditions.
* Ensure every screen is reachable and supports a clear back path.
* Ensure every screen supports a clear back path. These are navigation behaviors users expect across all platforms — regardless of UI.
<For example: For Screen Link to go back:
**Android**: Hardware/software back button always takes the user back one screen in the stack.
**iOS**: Top-left "Back" button or swipe gesture always goes to the previous screen.>

### <font color="#4285F4">Platform-Specific Transitions</font>
These are general interaction patterns specific to platforms, that are part of users mental model to transition from one screen to another.
Different platforms have different **UI metaphors and animations** for transitioning between screens or layers of interaction. Pair the correct `routes` to the appropriate platform-specific transitions as appropriate.
| TRANSITION PATTERN | iOS | Android |
| :--- | :--- | :--- |
| **Push (Stack)** | Left-to-right slide in | Slide in or fade |
| **Modal** | Slide up from bottom | Dialog box or bottom sheet |
| **Tab change** | Instant switch, no animation | Often slide/fade or direct switch |
| **Drawer** | Rarely used | Common (left slide-in nav) |
<br>

---
## <font color="#529E72">USER PROMPT</font>
I want to make a study planner for myself. I would strictlty follow it to study the college subjects and personal interest subjects. I also want this planner to include project timeline for my projects that are pending.

<br>

---
## <font color="#4285F4">SCREEN SPECIFICATION</font>



# Planning Dashboard

### Purpose
Provide a quick overview of upcoming academic and personal tasks, and offer access to core planning features.

### Primary Features
- Smart Deadline Balancer
- Personal-Academic Balance Dashboard
- Adaptive Task Breakdown Assistant

### Navigation Elements
- **Title:** `My Planner`
- **Components:**
  - Top Right Action Button
  - Top App Bar
  - Tab Bar
  - Inline Contextual Action

### Sections
- Upcoming Deadlines
- Your Balance Overview
- Quick Actions

### Component Placement Rules
The Tab Bar is used for primary global navigation (Home, Schedule, Progress, Prioritization, Settings/Profile) as per iOS Human Interface Guidelines, fixed at the bottom. The Top App Bar displays the screen title 'My Planner' and includes a primary action button 'Add New Task' on the top right, aligning with iOS conventions for contextual actions. Inline contextual actions like 'View All Tasks' and 'Adjust Balance' are placed within their respective content sections to maintain context and reduce cognitive load for the user.

### Linked Screens
- Add Task/Project
- My Schedule
- Progress Tracking
- Prioritization

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, Large
- **Body:** Poppins, Regular, Medium
- **CTA:** Montserrat, Semibold, Medium

### Color Usage
**Primary Color:**
- Top App Bar background
- Active Tab Bar icon/text
- Primary CTA buttons (e.g., 'Add New Task' button background)
- Section headers

**Accent Color:**
- Highlighting urgent deadlines
- Progress indicators (e.g., balance wheel segments)
- Interactive elements (e.g., 'View All Tasks' link, 'Adjust Balance' button text)

---

# Add Task/Project

### Purpose
Allow users to input details for a new academic assignment or personal project, including name, description, category, deadline, and linked materials.

### Primary Features
- Study Material Connection Hub
- Adaptive Task Breakdown Assistant

### Navigation Elements
- **Title:** `Add New Task`
- **Components:**
  - Modal Sheet
  - Inline Contextual Action
  - System Back Button
  - Top Right Action Button
  - Swipe Gesture
  - Top App Bar

### Sections
- Task Details
- Scheduling
- Materials
- Breakdown

### Component Placement Rules
A Modal Sheet is used for adding a new task to provide a focused, temporary context, allowing users to easily dismiss without losing their place on the dashboard, aligning with iOS HIG for task-oriented flows. The Top App Bar within the modal contains 'Cancel' (top-left) and 'Save' (top-right) actions, which is standard for iOS modals. Inline contextual actions like 'Add Material' and 'Suggest Steps' are placed near their respective input fields for clear context. 'Confirm Schedule' is a prominent primary action button at the bottom of the form. A Swipe Gesture allows for quick dismissal of the modal, enhancing user efficiency.

### Linked Screens
- Planning Dashboard
- My Schedule

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Semibold, Large
- **Body:** Poppins, Regular, Medium
- **CTA:** Montserrat, Semibold, Medium

### Color Usage
**Primary Color:**
- 'Save' button background
- Input field borders (on focus)
- Section titles

**Accent Color:**
- 'Add Material' icon
- 'Suggest Steps' button text
- Confirmation button (e.g., 'Confirm Schedule')

---

# My Schedule

### Purpose
Display the user's structured weekly study schedule, integrating academic and personal projects on a unified timeline.

### Primary Features
- Smart Deadline Balancer
- Study Material Connection Hub
- Customizable Planning Templates

### Navigation Elements
- **Title:** `My Schedule`
- **Components:**
  - Top App Bar
  - Top Right Action Button
  - Swipe Gesture
  - Inline Contextual Action
  - Tab Bar

### Sections
- This Week
- Next Week

### Component Placement Rules
The Tab Bar is used for global navigation to this screen. The Top App Bar displays the screen title and a 'Filter/View Options' button for customizing the schedule display, consistent with iOS design. Tasks on the timeline are interactive, allowing tap-to-view-details and drag-and-drop for prioritization, leveraging the 'Smart Deadline Balancer' design spec. A Swipe Gesture enables smooth navigation between different days or weeks on the schedule, enhancing usability and matching expected calendar interactions.

### Linked Screens
- Planning Dashboard
- Progress Tracking
- Prioritization
- Task Detail Modal
- Filter/View Options Modal

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, Large
- **Body:** Poppins, Regular, Small/Medium
- **CTA:** Montserrat, Semibold, Medium

### Color Usage
**Primary Color:**
- Active tab bar icon/text
- Calendar header/current day highlight
- Primary task blocks (academic)

**Accent Color:**
- Personal project task blocks
- Highlighting urgent tasks
- Drag-drop indicators
- Attachment icons

---

# Progress Tracking

### Purpose
Allow users to monitor and evaluate their progress on study tasks and projects, and visualize their academic-personal balance.

### Primary Features
- Focus Mode Time Tracker
- Personal-Academic Balance Dashboard
- Study Streak Motivator

### Navigation Elements
- **Title:** `My Progress`
- **Components:**
  - Top App Bar
  - Top Right Action Button
  - Tab Bar
  - Inline Contextual Action

### Sections
- Overall Balance
- Study Streaks
- Time Tracking Summary

### Component Placement Rules
The Tab Bar is used for global navigation to this screen. The Top App Bar displays the screen title and a 'Settings' button for customizing progress tracking preferences, aligning with iOS design principles. 'View Details' buttons are placed inline within each progress widget (e.g., balance wheel, streak calendar) to allow users to dive deeper into specific metrics, providing contextual access to information.

### Linked Screens
- Planning Dashboard
- My Schedule
- Prioritization
- Balance Detail Screen
- Streak History Screen

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, Large
- **Body:** Poppins, Regular, Medium
- **CTA:** Montserrat, Semibold, Medium

### Color Usage
**Primary Color:**
- Active tab bar icon/text
- Section titles
- Background of key progress cards

**Accent Color:**
- Balance wheel segments (personal projects)
- Study streak highlights (confetti animation)
- Progress bar fills
- Call-to-action text for 'View Details'

---

# Prioritization

### Purpose
Enable users to prioritize and re-organize tasks based on deadlines, importance, and available time using an interactive matrix and dynamic timeline.

### Primary Features
- Smart Deadline Balancer
- Adaptive Task Breakdown Assistant

### Navigation Elements
- **Title:** `Prioritize Tasks`
- **Components:**
  - Top Right Action Button
  - Tab Bar
  - Inline Contextual Action
  - Top App Bar

### Sections
- Urgent & Important
- Important but Not Urgent
- Urgent but Not Important
- Neither Urgent Nor Important
- Upcoming Deadlines

### Component Placement Rules
The Tab Bar is used for global navigation to this screen. The Top App Bar displays the screen title and a 'Sort/Filter' button to customize the task list, consistent with iOS design. Tasks within the priority matrix are interactive, supporting drag-and-drop for re-prioritization and tap-to-edit actions, leveraging the 'Smart Deadline Balancer' design spec. 'Confirm Changes' is a clear, prominent call to action button at the bottom of the screen.

### Linked Screens
- Planning Dashboard
- My Schedule
- Progress Tracking
- Task Detail Modal

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, Large
- **Body:** Poppins, Regular, Medium
- **CTA:** Montserrat, Semibold, Medium

### Color Usage
**Primary Color:**
- Active tab bar icon/text
- Quadrant borders/backgrounds (for high priority sections)
- Confirm Changes button

**Accent Color:**
- Highlighting urgent tasks within quadrants
- Drag-drop indicators
- Warning indicators for approaching deadlines


Strictly follow the below mentioned color scheme for generating UI. Be consistent.

Do not deviate.

Primary - "#007B7F"

Secondary - "#FF6F61"

Background- "#F4F4F4"
  """
}

# The endpoint URL
url = "http://127.0.0.1:8000/get-or-generate-files"

try:
    with requests.post(url, json=payload, stream=True) as r:
        r.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        if r.headers.get('Content-Type') == 'application/x-ndjson':
            print("INFO: Receiving a streaming response...")
            for line in r.iter_lines():
                if line:
                    try:
                        # Decode and parse each line as a JSON object
                        data = json.loads(line.decode('utf-8'))
                        print(json.dumps(data, indent=2))

                        # Check for completion or errors
                        if data.get("status") == "complete":
                            print("SUCCESS: Project generation is complete.")
                            break
                        elif data.get("status") == "error":
                            print(f"ERROR: {data.get('message')}")
                            break

                    except json.JSONDecodeError:
                        print(f"ERROR: Could not decode JSON from line: {line}")
        else:
            # Handle non-streaming (e.g., cached files) JSON response
            print("INFO: Received a standard JSON response (not a stream).")
            response_data = r.json()
            print(json.dumps(response_data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"FAILED to connect to the server: {e}")
