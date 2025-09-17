import json
import requests

# Payload for the request
payload = {
  "project_id": "test-project2-v3-test1",
  "file_id": "test-file-v3-test1",
  "prompt": """

## <font color="#E65B58">SYSTEM PROMPT FOR UX</font>

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
I am making a dog healthcare mobile app to track my dog's vaccination records. I want alerting feature so that I don't miss on vaccinations and vet visits.

<br>

---
## <font color="#4285F4">SCREEN SPECIFICATION</font>



# Screen: Home Screen

The main purpose of this screen is to to provide an overview of upcoming and past vaccination schedules and vet appointments, allowing quick access to details and actions.

---

## Key Features & Content Sections

### Primary Features
* Smart Vaccination Timeline
* Proactive Health Alert System
* One-Tap Appointment Coordinator

### On-Screen Sections & Grouping Logic
* **Upcoming Appointments**: Upcoming Appointments description not found.
* **Vaccination Timeline**: Vaccination Timeline description not found.
* **Quick Actions**: Quick Actions description not found.

---

## Layout & Hierarchy

* **Layout Type**: Collection_view.
* **Hierarchy**: The current dog's name/profile picture will be prominent at the top. 'Upcoming Appointments' section will use larger text and accent color for due dates to draw immediate attention, reflecting Emily's anxiety over missed appointments. Timeline entries will use color-coding (e.g., green for completed, yellow for upcoming, red for overdue) for quick visual scanning. Interactive elements like 'Add Record' will be clearly distinguishable.
* **Component Placement**: A top app bar will display the app title or dog's name, providing clear context. A top-right action button for 'Add Record' offers quick access to a frequent task. A bottom tab bar will be used for primary navigation between key sections: Home (Timeline), Health Records, Knowledge Hub, and possibly Profile/Settings. This follows iOS HIG for main navigation. Inline contextual actions (tapping a timeline event) are used to drill down into details, maintaining spatial sense.
* **Progressive Disclosure**: This is **enabled**.

---

## Navigation

### Navigation Logic
Users arrive here after login. Can navigate to other main sections via the bottom tab bar. Tapping an upcoming appointment on the timeline pushes to 'View Upcoming Appointment Details Screen'. Tapping the 'Add Record' button pushes to 'Access Add Record Form'.

### User Clarity
* **Where am I?**: On the Home screen, viewing your dog's vaccination timeline.
* **What can I do?**: View upcoming appointments, check past vaccinations, manage reminders, and quickly add new records.

### Navigation Title
*This screen's navigation bar title is **Paws Health**.*

### Navigation Components
* Top App Bar: ✅
* Inline Contextual Action: ✅
* Tab Bar: ✅
* Top Right Action Button: ✅

### Defined User Actions
* Add Record
* Profile/Settings
* View Details

### Routes from this Screen
* **Trigger**: User taps on an upcoming appointment card.
    * **From**: `Home Screen (Upcoming Appointment Card)`
    * **To**: `View Upcoming Appointment Details Screen`

* **Trigger**: User taps 'Add Record' button in top app bar.
    * **From**: `Home Screen (Add Record Button)`
    * **To**: `Access Add Record Form`

* **Trigger**: User taps 'Health Records' tab.
    * **From**: `Home Screen (Tab Bar: Health Records)`
    * **To**: `View Digital Health Passport`

* **Trigger**: User taps 'Knowledge Hub' tab.
    * **From**: `Home Screen (Tab Bar: Knowledge Hub)`
    * **To**: `Browse Content Categories`

### Linked Screens
* View Upcoming Appointment Details Screen
* View Digital Health Passport
* Browse Content Categories
* Access Add Record Form

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * App title
    * active tab bar icon/label (Home)
    * primary CTAs (e.g., 'Add Record' button background)
* **Accent Color Usage**:
    * Urgency indicators on timeline
    * notification badges
    * subtle animations for completed tasks

### Tone & Persona
* **Emotional Goals**: The screen should feel **alleviate anxiety, provide control, build assurance, promote efficiency.**.
* **Persona Notes**: Use clear, concise, and supportive language. Emphasize proactive management. For example, 'Your pet's health, simplified.' or 'Stay on track with Buddy's vaccinations.'

---

# Screen: View Upcoming Appointment Details Screen

The main purpose of this screen is to to provide detailed information about a specific upcoming vaccination or vet appointment and allow the user to take actions.

---

## Key Features & Content Sections

### Primary Features
* Smart Vaccination Timeline
* Proactive Health Alert System
* One-Tap Appointment Coordinator

### On-Screen Sections & Grouping Logic
* **Appointment Information**: Appointment Information description not found.
* **Actions**: Actions description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: Appointment name and date will be most prominent. Key actions like 'Acknowledge' will be primary CTAs using the primary color. Information will be presented in a clear, legible list format with appropriate spacing.
* **Component Placement**: A top app bar with a clear title and a back button (system back arrow) allows users to easily return to the Home screen. Primary actions like 'Add to Calendar', 'Reschedule', 'Acknowledge', and 'Snooze' are placed inline as prominent buttons, reflecting their importance for Emily's busy schedule. Less frequent actions like 'Cancel Appointment' are placed in an overflow menu to avoid clutter. Swipe gesture for back navigation provides a native iOS experience.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here by tapping an upcoming appointment on the 'Home Screen'. Returns to 'Home Screen' via back button/gesture or after acknowledging/snoozing. 'Add to Calendar' triggers native calendar integration. 'Reschedule' would push to a new screen for selecting a new date/time.

### User Clarity
* **Where am I?**: On the Appointment Details screen for [Appointment Name].
* **What can I do?**: View appointment specifics, add to calendar, reschedule, or acknowledge this reminder.

### Navigation Title
*This screen's navigation bar title is **Appointment Details**.*

### Navigation Components
* Top App Bar: ✅
* System Back Button: ✅
* Overflow Menu: ✅
* Swipe Gesture: ✅
* Inline Contextual Action: ✅

### Defined User Actions
* Add to Calendar
* Reschedule
* Acknowledge
* Snooze
* Cancel Appointment

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `View Upcoming Appointment Details Screen (Back Button/Gesture)`
    * **To**: `Home Screen`

* **Trigger**: User taps 'Add to Calendar'.
    * **From**: `View Upcoming Appointment Details Screen (Add to Calendar Button)`
    * **To**: `Native Calendar App`

* **Trigger**: User taps 'Reschedule'.
    * **From**: `View Upcoming Appointment Details Screen (Reschedule Button)`
    * **To**: `Reschedule Appointment Screen`

* **Trigger**: User taps 'Acknowledge'.
    * **From**: `View Upcoming Appointment Details Screen (Acknowledge Button)`
    * **To**: `Home Screen`

* **Trigger**: User taps 'Snooze'.
    * **From**: `View Upcoming Appointment Details Screen (Snooze Button)`
    * **To**: `Home Screen`

### Linked Screens
* Home Screen
* Reschedule Appointment Screen
* Confirmation Screen

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Action buttons ('Acknowledge', 'Add to Calendar')
    * navigation title
* **Accent Color Usage**:
    * Highlighting important dates/times
    * status indicators
    * subtle confirmation animations

### Tone & Persona
* **Emotional Goals**: The screen should feel **provide clear information, facilitate quick action, reduce anxiety about managing appointments.**.
* **Persona Notes**: Use direct, reassuring language. 'Your appointment for [Vaccine Name] is set.' 'Add to your calendar with one tap.'

---

# Screen: View Digital Health Passport

The main purpose of this screen is to to provide a secure, comprehensive overview of the dog's vaccination and health records, allowing easy access and verification.

---

## Key Features & Content Sections

### Primary Features
* Vaccination Record Vault
* Trust-Building Verification System

### On-Screen Sections & Grouping Logic
* **Current Pet: [Dog's Name]**: Current Pet: [Dog's Name] description not found.
* **Vaccination History**: Vaccination History description not found.
* **Other Health Records**: Other Health Records description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: The dog's name and a summary of their vaccination status (e.g., 'All up-to-date' or '1 overdue') will be at the top, using larger text. Each record entry in the list will clearly display the vaccination name, date, and a verification badge. Overdue records will be highlighted with the accent color. The 'Add Record' button will be prominent.
* **Component Placement**: A top app bar with the screen title and a prominent 'Add Record' button (or 'Share' icon) on the right for quick access to key functionalities. The bottom tab bar will include 'Health Records' as a primary navigation destination. Tapping on individual record entries uses inline contextual action to push to the 'View Vaccination Detail Screen'.
* **Progressive Disclosure**: This is **enabled**.

---

## Navigation

### Navigation Logic
Users navigate here via the bottom tab bar from any main screen. Tapping on a specific vaccination entry pushes to 'View Vaccination Detail Screen'. Tapping 'Add Record' pushes to 'Access Add Record Form'. 'Share' action would open a share sheet (modal).

### User Clarity
* **Where am I?**: On the Digital Health Passport screen for [Dog's Name].
* **What can I do?**: View all vaccination records, check health history, share records, or add new entries.

### Navigation Title
*This screen's navigation bar title is **Health Passport**.*

### Navigation Components
* Inline Contextual Action: ✅
* Tab Bar: ✅
* Top Right Action Button: ✅
* Top App Bar: ✅

### Defined User Actions
* Add Record
* Share
* View Details

### Routes from this Screen
* **Trigger**: User taps on a specific vaccination record entry.
    * **From**: `View Digital Health Passport (Vaccination Entry)`
    * **To**: `View Vaccination Detail Screen`

* **Trigger**: User taps 'Add Record' button in top app bar.
    * **From**: `View Digital Health Passport (Add Record Button)`
    * **To**: `Access Add Record Form`

* **Trigger**: User taps 'Share' icon.
    * **From**: `View Digital Health Passport (Share Button)`
    * **To**: `Share Sheet`

* **Trigger**: User taps 'Home' tab.
    * **From**: `View Digital Health Passport (Tab Bar: Home)`
    * **To**: `Home Screen`

* **Trigger**: User taps 'Knowledge Hub' tab.
    * **From**: `View Digital Health Passport (Tab Bar: Knowledge Hub)`
    * **To**: `Browse Content Categories`

### Linked Screens
* Home Screen
* Browse Content Categories
* View Vaccination Detail Screen
* Access Add Record Form
* Share Sheet

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Active tab bar icon/label (Health Records)
    * 'Add Record' button background
    * verification badges
* **Accent Color Usage**:
    * Highlighting overdue records
    * 'Share' icon
    * subtle lock/unlock animations for security

### Tone & Persona
* **Emotional Goals**: The screen should feel **build trust and confidence in record-keeping, provide a sense of safety and control over pet's health.**.
* **Persona Notes**: Use reassuring and professional language. 'Your pet's health records, always secure and accessible.' 'Verified for your peace of mind.'

---

# Screen: View Vaccination Detail Screen

The main purpose of this screen is to to display comprehensive details of a single vaccination record and offer options to share or edit it.

---

## Key Features & Content Sections

### Primary Features
* Vaccination Record Vault
* Trust-Building Verification System

### On-Screen Sections & Grouping Logic
* **Vaccination Details**: Vaccination Details description not found.
* **Proof of Vaccination**: Proof of Vaccination description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: Vaccination name will be the most prominent heading. Key details (date, vet) will use slightly larger/bolder text than other notes. The 'View Proof' button/link will be clearly visible if a document is present.
* **Component Placement**: A top app bar with a clear title and a back button for easy navigation back to the Health Passport. 'Share' and 'Edit' actions are placed in the top right for quick access, as these are common actions for a specific record. 'View Proof' is an inline action, appearing only if a document is attached. Swipe gesture for back navigation.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here by tapping a specific vaccination entry on the 'View Digital Health Passport' screen. Returns to 'View Digital Health Passport' via back button/gesture. 'Share' opens a native share sheet. 'Edit' pushes to an edit form (similar to 'Access Add Record Form').

### User Clarity
* **Where am I?**: On the Vaccination Detail screen for [Vaccination Name].
* **What can I do?**: Review vaccination details, view proof document, share this record, or edit information.

### Navigation Title
*This screen's navigation bar title is **Vaccination Details**.*

### Navigation Components
* System Back Button: ✅
* Swipe Gesture: ✅
* Top App Bar: ✅
* Top Right Action Button: ✅
* Inline Contextual Action: ✅

### Defined User Actions
* Share
* Edit
* View Proof

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `View Vaccination Detail Screen (Back Button/Gesture)`
    * **To**: `View Digital Health Passport`

* **Trigger**: User taps 'Share' icon.
    * **From**: `View Vaccination Detail Screen (Share Button)`
    * **To**: `Share Sheet`

* **Trigger**: User taps 'Edit' icon.
    * **From**: `View Vaccination Detail Screen (Edit Button)`
    * **To**: `Edit Vaccination Record Form`

* **Trigger**: User taps 'View Proof' link/button.
    * **From**: `View Vaccination Detail Screen (View Proof)`
    * **To**: `Document Viewer`

### Linked Screens
* View Digital Health Passport
* Edit Vaccination Record Form
* Share Sheet

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Edit' icon
    * 'Share' icon
* **Accent Color Usage**:
    * Verification badges
    * highlighting key data points like next due date (if applicable)

### Tone & Persona
* **Emotional Goals**: The screen should feel **reinforce trust in data accuracy, provide a sense of control over information.**.
* **Persona Notes**: Factual and clear. 'Verified record for [Vaccination Name].' 'Easily share or update this record.'

---

# Screen: Access Add Record Form

The main purpose of this screen is to to allow users to easily and accurately input details for a new vaccination record.

---

## Key Features & Content Sections

### Primary Features
* Vaccination Record Vault

### On-Screen Sections & Grouping Logic
* **Vaccination Details**: Vaccination Details description not found.
* **Proof (Optional)**: Proof (Optional) description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: Form fields will have clear labels and input areas. The 'Save' button will be a prominent CTA using the primary color. Auto-complete suggestions for vaccine names will be visually distinct.
* **Component Placement**: A top app bar with a clear title and a back button. A 'Save' button in the top right (or as a primary button at the bottom) provides a clear action to complete the form. Input fields are presented in a clear list format. 'Attach Document' is an inline action within the form. Swipe gesture for back navigation, potentially with a warning for unsaved data.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here by tapping 'Add Record' from 'Home Screen' or 'View Digital Health Passport'. 'Save' (or 'Next') pushes to 'Review and Confirm' screen. Back button/gesture or 'Cancel' returns to the previous screen, potentially with a discard warning.

### User Clarity
* **Where am I?**: On the Add New Vaccination Record screen.
* **What can I do?**: Enter vaccination details, attach proof, and save the new record.

### Navigation Title
*This screen's navigation bar title is **Add New Record**.*

### Navigation Components
* Top App Bar: ✅
* Inline Contextual Action: ✅
* System Back Button: ✅
* Top Right Action Button: ✅
* Swipe Gesture: ✅

### Defined User Actions
* Save
* Cancel
* Attach Document

### Routes from this Screen
* **Trigger**: User taps back button or swipes back (with discard warning).
    * **From**: `Access Add Record Form (Back Button/Gesture)`
    * **To**: `View Digital Health Passport`

* **Trigger**: User taps 'Save' or 'Next' button.
    * **From**: `Access Add Record Form (Save/Next Button)`
    * **To**: `Review and Confirm`

### Linked Screens
* View Digital Health Passport
* Review and Confirm

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Save' button background
* **Accent Color Usage**:
    * Input field borders when active
    * 'Attach Document' icon

### Tone & Persona
* **Emotional Goals**: The screen should feel **reduce cognitive load, provide a sense of efficiency and accuracy in data entry.**.
* **Persona Notes**: Use clear, instructional language. 'Enter details for [Dog's Name]'s new vaccination.' 'Quickly add records to keep everything up-to-date.'

---

# Screen: Review and Confirm

The main purpose of this screen is to to allow the user to review all entered vaccination details before final submission, ensuring accuracy.

---

## Key Features & Content Sections

### Primary Features
* Vaccination Record Vault

### On-Screen Sections & Grouping Logic
* **Vaccination Details**: Vaccination Details description not found.
* **Veterinary Information**: Veterinary Information description not found.
* **Attached Documents**: Attached Documents description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: The screen title and 'Confirm & Save' button will be prominent. Each detail will be clearly labeled, with the entered value in a slightly bolder font. 'Edit' actions will be subtle but clear.
* **Component Placement**: A top app bar with a clear title and a back button to allow users to go back and edit the form. A prominent 'Confirm & Save' button at the bottom of the screen to finalize the action. Small 'Edit' buttons or icons next to each section of details allow for quick adjustments, as per UX tip. Swipe gesture for back navigation.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here from 'Access Add Record Form' after entering details. Tapping 'Confirm & Save' pushes to 'Receive Record Confirmation'. Back button/gesture or 'Edit' returns to 'Access Add Record Form'.

### User Clarity
* **Where am I?**: On the Review and Confirm screen for the new vaccination record.
* **What can I do?**: Review all details, make quick edits, or confirm and save the record.

### Navigation Title
*This screen's navigation bar title is **Review & Confirm**.*

### Navigation Components
* Inline Contextual Action: ✅
* Swipe Gesture: ✅
* System Back Button: ✅
* Top App Bar: ✅

### Defined User Actions
* Confirm & Save
* Edit

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `Review and Confirm (Back Button/Gesture)`
    * **To**: `Access Add Record Form`

* **Trigger**: User taps 'Edit' button next to a section.
    * **From**: `Review and Confirm (Edit Button)`
    * **To**: `Access Add Record Form`

* **Trigger**: User taps 'Confirm & Save' button.
    * **From**: `Review and Confirm (Confirm & Save Button)`
    * **To**: `Receive Record Confirmation`

### Linked Screens
* Access Add Record Form
* Receive Record Confirmation

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Confirm & Save' button background
* **Accent Color Usage**:
    * Small 'Edit' icons/text
    * highlighting any critical warnings if data is incomplete

### Tone & Persona
* **Emotional Goals**: The screen should feel **provide a sense of control and finality, build confidence in the accuracy of the record.**.
* **Persona Notes**: Clear, reassuring, and action-oriented. 'Please review your entry before saving.' 'Your record will be securely added.'

---

# Screen: Receive Record Confirmation

The main purpose of this screen is to to confirm to the user that their new vaccination record has been successfully added and provide clear next steps.

---

## Key Features & Content Sections

### Primary Features
* Vaccination Record Vault
* Trust-Building Verification System

---

## Layout & Hierarchy

* **Layout Type**: Collection_view.
* **Hierarchy**: A large, central success message (e.g., 'Record Added!') with a celebratory animation will dominate the screen. The primary CTA 'Go to Health Passport' will be visually most prominent. Subtle text reinforcing security and trust will be included.
* **Component Placement**: A top app bar with a celebratory title. No back button, as this is a confirmation screen; the user should be guided to next actions. Prominent inline buttons offer clear next steps: 'Go to Health Passport' as the primary action, and 'View Record' as a secondary option.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here from 'Review and Confirm' after successful submission. 'Go to Health Passport' navigates to 'View Digital Health Passport' (replacing the stack). 'View Record' navigates to 'View Vaccination Detail Screen' for the newly added record.

### User Clarity
* **Where am I?**: On the Record Confirmation screen.
* **What can I do?**: View the newly added record, return to health passport, or continue managing records.

### Navigation Title
*This screen's navigation bar title is **Record Added!**.*

### Navigation Components
* Inline Contextual Action: ✅
* Top App Bar: ✅

### Defined User Actions
* View Record
* Go to Health Passport

### Routes from this Screen
* **Trigger**: User taps 'Go to Health Passport' button.
    * **From**: `Receive Record Confirmation (Go to Health Passport Button)`
    * **To**: `View Digital Health Passport`

* **Trigger**: User taps 'View Record' button.
    * **From**: `Receive Record Confirmation (View Record Button)`
    * **To**: `View Vaccination Detail Screen`

### Linked Screens
* View Digital Health Passport
* View Vaccination Detail Screen

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Extra Bold, Very Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Go to Health Passport' button background
* **Accent Color Usage**:
    * Confirmation animation (e.g., checkmark)
    * 'View Record' button text

### Tone & Persona
* **Emotional Goals**: The screen should feel **provide a sense of relief and accomplishment, reinforce trust and reliability.**.
* **Persona Notes**: Positive, encouraging, and clear about the next steps. 'Great job, Emily! [Dog's Name]'s record is now updated.' 'You're doing a fantastic job keeping your pet healthy.'

---

# Screen: Browse Content Categories

The main purpose of this screen is to to allow users to explore veterinarian-verified educational content categorized for easy discovery.

---

## Key Features & Content Sections

### Primary Features
* Vet-Verified Knowledge Hub

### On-Screen Sections & Grouping Logic
* **Explore Topics**: Explore Topics description not found.
* **Get Personalized Advice**: Get Personalized Advice description not found.

---

## Layout & Hierarchy

* **Layout Type**: Grid.
* **Hierarchy**: Category cards will use images and clear titles, with trust badges to emphasize vet verification. The 'Get Personalized Advice' section will be visually distinct and prominent, possibly using a larger card or a primary CTA. Titles will use the secondary font for emphasis.
* **Component Placement**: A top app bar with a clear title. A search icon in the top right allows users to quickly find specific topics. The bottom tab bar will include 'Knowledge Hub' as a primary navigation destination. Category cards are interactive, leading to content. A dedicated card/button for 'Vaccination Decision Assistant' is prominent.
* **Progressive Disclosure**: This is **enabled**.

---

## Navigation

### Navigation Logic
Users navigate here via the bottom tab bar from any main screen. Tapping a category card pushes to 'View Educational Articles/Videos'. Tapping 'Access Decision Assistant' pushes to 'Input Dog's Profile Details'.

### User Clarity
* **Where am I?**: On the Knowledge Hub screen, browsing educational categories.
* **What can I do?**: Select a category to learn more about vaccinations and dog health, or access personalized advice.

### Navigation Title
*This screen's navigation bar title is **Knowledge Hub**.*

### Navigation Components
* Tab Bar: ✅
* Inline Contextual Action: ✅
* Top App Bar: ✅
* Top Right Action Button: ✅

### Defined User Actions
* Search
* Access Decision Assistant

### Routes from this Screen
* **Trigger**: User taps on an educational content category card.
    * **From**: `Browse Content Categories (Category Card)`
    * **To**: `View Educational Articles/Videos`

* **Trigger**: User taps 'Access Decision Assistant' button.
    * **From**: `Browse Content Categories (Access Decision Assistant Button)`
    * **To**: `Input Dog's Profile Details`

* **Trigger**: User taps 'Search' icon in top app bar.
    * **From**: `Browse Content Categories (Search Icon)`
    * **To**: `Search Results Screen`

* **Trigger**: User taps 'Home' tab.
    * **From**: `Browse Content Categories (Tab Bar: Home)`
    * **To**: `Home Screen`

* **Trigger**: User taps 'Health Records' tab.
    * **From**: `Browse Content Categories (Tab Bar: Health Records)`
    * **To**: `View Digital Health Passport`

### Linked Screens
* Home Screen
* View Digital Health Passport
* View Educational Articles/Videos
* Input Dog's Profile Details
* Search Results Screen

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Active tab bar icon/label (Knowledge Hub)
    * 'Access Decision Assistant' button background
* **Accent Color Usage**:
    * Trust badges on category cards
    * subtle pulse animation for new content

### Tone & Persona
* **Emotional Goals**: The screen should feel **empower users with knowledge, build trust in information, reduce uncertainty.**.
* **Persona Notes**: Informative, authoritative yet approachable. 'Learn more about your dog's health.' 'Expert advice at your fingertips.'

---

# Screen: View Educational Articles/Videos

The main purpose of this screen is to to present detailed, veterinarian-verified educational content (articles or videos) in an engaging and easily digestible format.

---

## Key Features & Content Sections

### Primary Features
* Vet-Verified Knowledge Hub
* Visual Vaccination Explainer

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: Article title will be prominent. Headings within the article will use the secondary font for structure. Images/videos will be appropriately sized and placed for readability. 'Vet-Verified' badge will be clearly visible.
* **Component Placement**: A top app bar with the article title and a back button to return to 'Browse Content Categories'. 'Share' and 'Save for Offline' actions are placed in the top right for easy access. Inline actions for content rating and feedback loop. Swipe gesture for back navigation.
* **Progressive Disclosure**: This is **enabled**.

---

## Navigation

### Navigation Logic
Users navigate here by tapping a content card on 'Browse Content Categories'. Returns to 'Browse Content Categories' via back button/gesture. 'Share' opens a native share sheet.

### User Clarity
* **Where am I?**: On the educational content screen: '[Article/Video Title]'.
* **What can I do?**: Read the article, watch the video, save for later, or provide feedback.

### Navigation Title
*This screen's navigation bar title is **[Article/Video Title]**.*

### Navigation Components
* Swipe Gesture: ✅
* System Back Button: ✅
* Top Right Action Button: ✅
* Top App Bar: ✅
* Inline Contextual Action: ✅

### Defined User Actions
* Share
* Save for Offline
* Rate Content

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `View Educational Articles/Videos (Back Button/Gesture)`
    * **To**: `Browse Content Categories`

* **Trigger**: User taps 'Share' icon.
    * **From**: `View Educational Articles/Videos (Share Button)`
    * **To**: `Share Sheet`

* **Trigger**: User taps to expand an infographic.
    * **From**: `View Educational Articles/Videos (Interactive Infographic)`
    * **To**: `Expanded Infographic View`

### Linked Screens
* Browse Content Categories
* Share Sheet

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Save for Offline' toggle/icon
    * 'Share' icon
* **Accent Color Usage**:
    * Highlighting key terms
    * interactive elements in infographics
    * content rating stars

### Tone & Persona
* **Emotional Goals**: The screen should feel **empower users with clear, reliable information, build confidence in decision-making.**.
* **Persona Notes**: Educational, clear, and reassuring. 'Understanding [Topic Name].' 'Backed by veterinary experts.'

---

# Screen: Input Dog's Profile Details

The main purpose of this screen is to to collect specific details about the user's dog to provide personalized vaccination recommendations.

---

## Key Features & Content Sections

### Primary Features
* Vet-Verified Knowledge Hub

### On-Screen Sections & Grouping Logic
* **Your Dog's Profile**: Your Dog's Profile description not found.
* **Lifestyle & Location**: Lifestyle & Location description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: Clear labels for each input field. The 'Get Recommendations' button will be the primary CTA. The 'Auto-fill' option will be visually distinct but secondary.
* **Component Placement**: A top app bar with a clear title and a back button to return to 'Browse Content Categories'. A prominent 'Get Recommendations' button at the bottom to proceed. An 'Auto-fill from Profile' option is placed inline near the input fields to save user effort. Swipe gesture for back navigation.
* **Progressive Disclosure**: This is **disabled**.

---

## Navigation

### Navigation Logic
Users navigate here by tapping 'Engage with Decision Assistant' from 'Browse Content Categories'. 'Get Recommendations' pushes to 'Receive Personalized Insights'. Back button/gesture returns to 'Browse Content Categories'.

### User Clarity
* **Where am I?**: On the Vaccination Decision Assistant setup screen.
* **What can I do?**: Enter your dog's details to get personalized vaccination advice.

### Navigation Title
*This screen's navigation bar title is **Decision Assistant**.*

### Navigation Components
* Top App Bar: ✅
* Swipe Gesture: ✅
* System Back Button: ✅
* Inline Contextual Action: ✅

### Defined User Actions
* Get Recommendations
* Auto-fill from Profile

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `Input Dog's Profile Details (Back Button/Gesture)`
    * **To**: `Browse Content Categories`

* **Trigger**: User taps 'Get Recommendations' button.
    * **From**: `Input Dog's Profile Details (Get Recommendations Button)`
    * **To**: `Receive Personalized Insights`

### Linked Screens
* Browse Content Categories
* Receive Personalized Insights

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Get Recommendations' button background
* **Accent Color Usage**:
    * Input field borders when active
    * 'Auto-fill' link

### Tone & Persona
* **Emotional Goals**: The screen should feel **provide a sense of control over personalized advice, build confidence in the relevance of information.**.
* **Persona Notes**: Guided, encouraging. 'Tell us about [Dog's Name] for tailored advice.' 'We'll help you make the best choices.'

---

# Screen: Receive Personalized Insights

The main purpose of this screen is to to present personalized vaccination recommendations and explanations based on the dog's profile.

---

## Key Features & Content Sections

### Primary Features
* Vet-Verified Knowledge Hub

### On-Screen Sections & Grouping Logic
* **Recommendations for [Dog's Name]**: Recommendations for [Dog's Name] description not found.
* **Understanding the Recommendations**: Understanding the Recommendations description not found.
* **Related Topics**: Related Topics description not found.

---

## Layout & Hierarchy

* **Layout Type**: List.
* **Hierarchy**: The main recommendation summary will be prominent. Each recommendation will be clearly stated, with its reasoning explained below. 'Learn More' links will be visually distinct. Trust badges will reinforce the vet-verified nature of the advice.
* **Component Placement**: A top app bar with a clear title and a back button to return to 'Input Dog's Profile Details'. A 'Share Insights' button in the top right allows users to easily share this personalized information. 'Learn More' links are placed inline with each recommendation to provide deeper context. Swipe gesture for back navigation.
* **Progressive Disclosure**: This is **enabled**.

---

## Navigation

### Navigation Logic
Users navigate here from 'Input Dog's Profile Details' after submitting their dog's information. Returns to 'Input Dog's Profile Details' via back button/gesture. 'Learn More' pushes to relevant 'View Educational Articles/Videos'. 'Share Insights' opens a native share sheet.

### User Clarity
* **Where am I?**: On the Personalized Vaccination Insights screen for [Dog's Name].
* **What can I do?**: Review tailored recommendations, understand the reasoning, or explore related topics.

### Navigation Title
*This screen's navigation bar title is **Your Personalized Insights**.*

### Navigation Components
* System Back Button: ✅
* Swipe Gesture: ✅
* Inline Contextual Action: ✅
* Top App Bar: ✅
* Top Right Action Button: ✅

### Defined User Actions
* Share Insights
* Learn More

### Routes from this Screen
* **Trigger**: User taps back button or swipes back.
    * **From**: `Receive Personalized Insights (Back Button/Gesture)`
    * **To**: `Input Dog's Profile Details`

* **Trigger**: User taps 'Share Insights' icon.
    * **From**: `Receive Personalized Insights (Share Insights Button)`
    * **To**: `Share Sheet`

* **Trigger**: User taps 'Learn More' link next to a recommendation.
    * **From**: `Receive Personalized Insights (Learn More Link)`
    * **To**: `View Educational Articles/Videos`

### Linked Screens
* Input Dog's Profile Details
* View Educational Articles/Videos
* Share Sheet

---

## Styling & Tone

### Typography
* **Primary Font**: Poppins
* **Secondary Font**: Montserrat
* **Text Styles**:
    * **Title**: Montserrat, Bold, Large
    * **Body**: Poppins, Regular, Medium
    * **CTA**: Poppins, Semi-bold, Medium, White text on Forest Green background

### Color Usage
* **Primary Color Usage**:
    * Navigation title
    * 'Share Insights' icon
* **Accent Color Usage**:
    * Highlighting key recommendations
    * 'Learn More' links
    * trust badges

### Tone & Persona
* **Emotional Goals**: The screen should feel **provide clarity and confidence in health decisions, empower users with personalized knowledge.**.
* **Persona Notes**: Authoritative, supportive, and clear. 'Here are the best vaccination insights for [Dog's Name].' 'Empowering you to make informed choices.'


Strictly follow the below mentioned color scheme for generating UI. Be consistent.

Do not deviate.

Primary - "#228B22"

Secondary - "#FFD700"

Background- "#F8F8F8"
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
