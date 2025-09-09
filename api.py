import json
import requests

# payload = {
#     "project_id": "meowmeow-project",
#     "file_id": "meowmeow-file",
#     "prompt": """
# <screen_specifications>
# ---
# ## <font color="#529E72">USER PROMPT</font>
# I am building a chatbot to help users easily claim insurance by removing the confusion, delays, and stress often associated with the process. Many users feel lost in jargon, abandon claims midway, or struggle with uploading documents and tracking progress. The visual design is chat-first and emotionally supportive, using soft colors, large touch-friendly buttons, clear progress indicators, and reassuring microcopy to build trust and reduce anxiety. It feels more like texting a helpful friend than navigating a bureaucratic form.

# <br>

# ---
# ## <font color="#4285F4">SCREEN SPECIFICATION</font>



# # Home Screen

# ### Purpose
# To provide an entry point for users to start new claims, track existing ones, or access support.

# ### Primary Features
# - Process Simplification Wizard
# - Visual Claim Timeline

# ### Navigation Elements
# - **Title:** `Virtual Claims Companion`
# - **Components:**
#   - Top App Bar
#   - Tab Bar
#   - Inline Contextual Action
#   - Top Right Action Button

# ### Sections
# - What would you like to do?
# - Quick Actions

# ### Component Placement Rules
# Top App Bar for screen title ('Virtual Claims Companion') and a global 'Settings' action (top-right). Tab Bar at the bottom for primary navigation: Home, My Claims, Profile. This aligns with iOS HIG for switching between distinct high-level sections. Main actions ('Start New Claim', 'Track My Claims') are presented as prominent inline buttons, guiding the user to their primary goals. FABs are avoided as per iOS guidelines.

# ### Linked Screens
# - Select Claim Type
# - Select Claim to View
# - Profile Screen
# - Settings Screen

# ### Progressive Disclosure
# **No**

# ### Text Styles
# - **Title:** Montserrat, Bold, 24pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - App title in Top App Bar
# - 'Start New Claim' button background
# - Active tab bar icon/label

# **Accent Color:**
# - 'Track My Claims' button border/text
# - Small icons for quick actions
# - Potential notification badges

# ---

# # Select Claim Type

# ### Purpose
# To allow the user to choose the specific type of insurance claim they wish to file.

# ### Primary Features
# - Process Simplification Wizard

# ### Navigation Elements
# - **Title:** `Start a New Claim`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action
#   - Swipe Gesture
#   - System Back Button

# ### Sections
# - Choose your claim type

# ### Component Placement Rules
# Top App Bar with a clear title 'Start a New Claim' and a top-left back arrow for navigation back to the Home Screen, adhering to iOS push navigation patterns. Claim types presented as prominent, tappable inline buttons, making selection straightforward. System back button/swipe gesture supported for intuitive navigation.

# ### Linked Screens
# - Home Screen
# - Claim Details Input Screen

# ### Progressive Disclosure
# **No**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - Back button icon
# - Selected claim type button background

# **Accent Color:**
# - Unselected claim type button borders/text (if styled as outlines)
# - Subtle highlight on tap

# ---

# # Upload Supporting Documents

# ### Purpose
# To guide the user through uploading necessary documents for their claim, ensuring correct format and content.

# ### Primary Features
# - Document Upload Assistant
# - Jargon Translator

# ### Navigation Elements
# - **Title:** `Upload Documents`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action
#   - Swipe Gesture
#   - System Back Button

# ### Sections
# - Required Documents
# - Uploaded Files

# ### Component Placement Rules
# Top App Bar with title and back button for standard iOS navigation. A prominent 'Upload Document' button (inline) to initiate the document upload process, aligning with the Document Upload Assistant's camera icon with '+' affordance. A 'Next' button (inline, at the bottom) to proceed after documents are uploaded.

# ### Linked Screens
# - Claim Details Input Screen
# - Review Claim Summary
# - Jargon Translator Modal
# - Camera/File Picker (System)

# ### Progressive Disclosure
# **Yes**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - Back button icon
# - 'Next' button background
# - Progress ring for upload

# **Accent Color:**
# - 'Upload Document' button icon (camera with '+')
# - Error states for document validation
# - Confetti animation on success

# ---

# # Review Claim Summary

# ### Purpose
# To allow the user to review all entered details of their claim before final submission.

# ### Primary Features
# - Jargon Translator

# ### Navigation Elements
# - **Title:** `Review Your Claim`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action
#   - Swipe Gesture
#   - System Back Button

# ### Sections
# - Incident Details
# - Uploaded Documents
# - Contact Information
# - Policy Details

# ### Component Placement Rules
# Top App Bar with title and back button for standard iOS navigation. 'Edit' buttons placed inline next to each claim section, allowing easy modification of specific details. A prominent 'Submit Claim' button at the bottom, acting as the final call to action.

# ### Linked Screens
# - Upload Supporting Documents
# - Claim Confirmation & Progress
# - Jargon Translator Modal
# - Edit Claim Details (Modal)

# ### Progressive Disclosure
# **No**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - Back button icon
# - 'Submit Claim' button background

# **Accent Color:**
# - 'Edit' icons/text
# - Underlined jargon terms

# ---

# # Claim Confirmation & Progress

# ### Purpose
# To confirm successful claim submission and immediately display the initial progress of the claim.

# ### Primary Features
# - Visual Claim Timeline

# ### Navigation Elements
# - **Title:** `Claim Submitted!`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action
#   - Top Right Action Button

# ### Sections
# - Your Claim is Submitted!
# - Current Progress

# ### Component Placement Rules
# Top App Bar with a celebratory title and a 'Done' or 'Home' button in the top-right, allowing the user to exit the flow gracefully, adhering to iOS completion patterns. No back button, as the task is complete. The Visual Claim Timeline is prominently displayed inline. An inline 'View Full Timeline' button to navigate to the dedicated full timeline screen.

# ### Linked Screens
# - Home Screen
# - Visual Claim Progress Timeline

# ### Progressive Disclosure
# **Yes**

# ### Text Styles
# - **Title:** Montserrat, Bold, 24pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - 'Done' button
# - Active stage indicator in timeline

# **Accent Color:**
# - Confetti animation (from Document Upload Assistant design spec, applied here for success)
# - Milestone celebrations on timeline

# ---

# # Select Claim to View

# ### Purpose
# To display a list of the user's active and past claims, allowing them to select one to view its details.

# ### Navigation Elements
# - **Title:** `My Claims`
# - **Components:**
#   - Top App Bar
#   - Tab Bar
#   - Inline Contextual Action
#   - Top Right Action Button

# ### Sections
# - Active Claims
# - Past Claims

# ### Component Placement Rules
# Top App Bar with title 'My Claims'. A 'Start New Claim' button in the top-right provides a quick way to initiate a new claim from this view, and a 'Filter' option for managing the list. Tab Bar at the bottom, with 'My Claims' as the active tab, maintaining global navigation consistency. Each claim in the list is an inline tappable element.

# ### Linked Screens
# - Home Screen
# - Visual Claim Progress Timeline
# - Select Claim Type
# - Filter Claims (Modal)

# ### Progressive Disclosure
# **Yes**

# ### Text Styles
# - **Title:** Montserrat, Bold, 24pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - Active tab bar icon/label
# - 'Start New Claim' button text (if outline) or background

# **Accent Color:**
# - Status indicators for active claims
# - Small icons within list items

# ---

# # Visual Claim Progress Timeline

# ### Purpose
# To provide a detailed, interactive visual timeline of a specific claim's progress, showing current status, completed steps, and future actions.

# ### Primary Features
# - Visual Claim Timeline
# - Jargon Translator
# - Partner Support Mode

# ### Navigation Elements
# - **Title:** `Claim [Claim ID] Progress`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action
#   - Top Right Action Button
#   - Swipe Gesture
#   - System Back Button

# ### Sections
# - Your Claim Journey
# - Next Steps

# ### Component Placement Rules
# Top App Bar with a clear title (Claim ID) and a back button. A 'Share with Partner' button in the top-right, leveraging the Partner Support Mode feature. The Visual Claim Timeline is the central, interactive element, horizontal scrollable. Tapping on a timeline stage expands details inline or via a bottom sheet.

# ### Linked Screens
# - Select Claim to View
# - Select Helper & Set Permissions
# - Jargon Translator Modal
# - Expanded Stage Details (Bottom Sheet)

# ### Progressive Disclosure
# **Yes**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - Back button icon
# - Pulsing 'current stage' indicator
# - Completed stage checkmarks

# **Accent Color:**
# - Estimated completion times
# - Haptic feedback on stage completion
# - 'Share with Partner' icon

# ---

# # Select Helper & Set Permissions

# ### Purpose
# To allow the primary user to invite a helper (partner) and define specific permissions for their access to the claim.

# ### Primary Features
# - Partner Support Mode
# - Guided Co-Browsing Support

# ### Navigation Elements
# - **Title:** `Invite a Helper`
# - **Components:**
#   - Top App Bar
#   - Modal Sheet
#   - Inline Contextual Action
#   - Top Right Action Button
#   - Swipe Gesture
#   - System Back Button

# ### Sections
# - Invite a Contact
# - Set Permissions

# ### Component Placement Rules
# Presented as a modal sheet (full-screen) for a focused, temporary task, with a 'Cancel' button in the top-left, aligning with iOS modal patterns. Inline elements for contact selection and permission toggles. A prominent 'Send Invitation' button at the bottom.

# ### Linked Screens
# - Visual Claim Progress Timeline
# - Invitation Sent Confirmation (Toast/Alert)

# ### Progressive Disclosure
# **No**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Modal title
# - 'Send Invitation' button background
# - Active toggle states

# **Accent Color:**
# - Toggle switches
# - Subtle highlights on interactive elements

# ---

# # Helper Accepts Invitation

# ### Purpose
# To provide the invited helper (David) with a clear interface to accept the invitation and access the shared claim, with an option to activate 'Helper View'.

# ### Primary Features
# - Partner Support Mode

# ### Navigation Elements
# - **Title:** `Invitation from Emily`
# - **Components:**
#   - Top App Bar
#   - Inline Contextual Action

# ### Sections
# - You've been invited!
# - Access Options

# ### Component Placement Rules
# Top App Bar with a clear, personalized title ('Invitation from Emily'). A prominent 'Accept Invitation' button. An inline toggle for 'Activate Helper View' (Partner Support Mode).

# ### Linked Screens
# - Helper Claim View (with Partner Support Mode active)

# ### Progressive Disclosure
# **No**

# ### Text Styles
# - **Title:** Montserrat, SemiBold, 20pt
# - **Body:** Poppins, Regular, 16pt
# - **CTA:** Poppins, SemiBold, 18pt

# ### Color Usage
# **Primary Color:**
# - Top App Bar title
# - 'Accept Invitation' button background
# - Active toggle state for Helper View

# **Accent Color:**
# - Toggle switch for Helper View
# - Subtle highlights


# Strictly follow the below mentioned color scheme for generating UI. Be consistent. 

# Do not deviate.

# Primary - "#A3C1DA"

# Secondary - "#F6A3A3"

# Background- "#F7F7F7"
# </screen_specifications>

# """
# }

# response = requests.post("http://127.0.0.1:8000/template", json=payload)

payload = {
  "project_id": "meowmeow-project",
  "file_id": "meowmeow-file",
  "ui_prompt": """
<screen_specifications>
---
## <font color="#529E72">USER PROMPT</font>
I am building a chatbot to help users easily claim insurance by removing the confusion, delays, and stress often associated with the process. Many users feel lost in jargon, abandon claims midway, or struggle with uploading documents and tracking progress. The visual design is chat-first and emotionally supportive, using soft colors, large touch-friendly buttons, clear progress indicators, and reassuring microcopy to build trust and reduce anxiety. It feels more like texting a helpful friend than navigating a bureaucratic form.

<br>

---
## <font color="#4285F4">SCREEN SPECIFICATION</font>



# Home Screen

### Purpose
To provide an entry point for users to start new claims, track existing ones, or access support.

### Primary Features
- Process Simplification Wizard
- Visual Claim Timeline

### Navigation Elements
- **Title:** `Virtual Claims Companion`
- **Components:**
  - Top App Bar
  - Tab Bar
  - Inline Contextual Action
  - Top Right Action Button

### Sections
- What would you like to do?
- Quick Actions

### Component Placement Rules
Top App Bar for screen title ('Virtual Claims Companion') and a global 'Settings' action (top-right). Tab Bar at the bottom for primary navigation: Home, My Claims, Profile. This aligns with iOS HIG for switching between distinct high-level sections. Main actions ('Start New Claim', 'Track My Claims') are presented as prominent inline buttons, guiding the user to their primary goals. FABs are avoided as per iOS guidelines.

### Linked Screens
- Select Claim Type
- Select Claim to View
- Profile Screen
- Settings Screen

### Progressive Disclosure
**No**

### Text Styles
- **Title:** Montserrat, Bold, 24pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- App title in Top App Bar
- 'Start New Claim' button background
- Active tab bar icon/label

**Accent Color:**
- 'Track My Claims' button border/text
- Small icons for quick actions
- Potential notification badges

---

# Select Claim Type

### Purpose
To allow the user to choose the specific type of insurance claim they wish to file.

### Primary Features
- Process Simplification Wizard

### Navigation Elements
- **Title:** `Start a New Claim`
- **Components:**
  - Top App Bar
  - Inline Contextual Action
  - Swipe Gesture
  - System Back Button

### Sections
- Choose your claim type

### Component Placement Rules
Top App Bar with a clear title 'Start a New Claim' and a top-left back arrow for navigation back to the Home Screen, adhering to iOS push navigation patterns. Claim types presented as prominent, tappable inline buttons, making selection straightforward. System back button/swipe gesture supported for intuitive navigation.

### Linked Screens
- Home Screen
- Claim Details Input Screen

### Progressive Disclosure
**No**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- Back button icon
- Selected claim type button background

**Accent Color:**
- Unselected claim type button borders/text (if styled as outlines)
- Subtle highlight on tap

---

# Upload Supporting Documents

### Purpose
To guide the user through uploading necessary documents for their claim, ensuring correct format and content.

### Primary Features
- Document Upload Assistant
- Jargon Translator

### Navigation Elements
- **Title:** `Upload Documents`
- **Components:**
  - Top App Bar
  - Inline Contextual Action
  - Swipe Gesture
  - System Back Button

### Sections
- Required Documents
- Uploaded Files

### Component Placement Rules
Top App Bar with title and back button for standard iOS navigation. A prominent 'Upload Document' button (inline) to initiate the document upload process, aligning with the Document Upload Assistant's camera icon with '+' affordance. A 'Next' button (inline, at the bottom) to proceed after documents are uploaded.

### Linked Screens
- Claim Details Input Screen
- Review Claim Summary
- Jargon Translator Modal
- Camera/File Picker (System)

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- Back button icon
- 'Next' button background
- Progress ring for upload

**Accent Color:**
- 'Upload Document' button icon (camera with '+')
- Error states for document validation
- Confetti animation on success

---

# Review Claim Summary

### Purpose
To allow the user to review all entered details of their claim before final submission.

### Primary Features
- Jargon Translator

### Navigation Elements
- **Title:** `Review Your Claim`
- **Components:**
  - Top App Bar
  - Inline Contextual Action
  - Swipe Gesture
  - System Back Button

### Sections
- Incident Details
- Uploaded Documents
- Contact Information
- Policy Details

### Component Placement Rules
Top App Bar with title and back button for standard iOS navigation. 'Edit' buttons placed inline next to each claim section, allowing easy modification of specific details. A prominent 'Submit Claim' button at the bottom, acting as the final call to action.

### Linked Screens
- Upload Supporting Documents
- Claim Confirmation & Progress
- Jargon Translator Modal
- Edit Claim Details (Modal)

### Progressive Disclosure
**No**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- Back button icon
- 'Submit Claim' button background

**Accent Color:**
- 'Edit' icons/text
- Underlined jargon terms

---

# Claim Confirmation & Progress

### Purpose
To confirm successful claim submission and immediately display the initial progress of the claim.

### Primary Features
- Visual Claim Timeline

### Navigation Elements
- **Title:** `Claim Submitted!`
- **Components:**
  - Top App Bar
  - Inline Contextual Action
  - Top Right Action Button

### Sections
- Your Claim is Submitted!
- Current Progress

### Component Placement Rules
Top App Bar with a celebratory title and a 'Done' or 'Home' button in the top-right, allowing the user to exit the flow gracefully, adhering to iOS completion patterns. No back button, as the task is complete. The Visual Claim Timeline is prominently displayed inline. An inline 'View Full Timeline' button to navigate to the dedicated full timeline screen.

### Linked Screens
- Home Screen
- Visual Claim Progress Timeline

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, 24pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- 'Done' button
- Active stage indicator in timeline

**Accent Color:**
- Confetti animation (from Document Upload Assistant design spec, applied here for success)
- Milestone celebrations on timeline

---

# Select Claim to View

### Purpose
To display a list of the user's active and past claims, allowing them to select one to view its details.

### Navigation Elements
- **Title:** `My Claims`
- **Components:**
  - Top App Bar
  - Tab Bar
  - Inline Contextual Action
  - Top Right Action Button

### Sections
- Active Claims
- Past Claims

### Component Placement Rules
Top App Bar with title 'My Claims'. A 'Start New Claim' button in the top-right provides a quick way to initiate a new claim from this view, and a 'Filter' option for managing the list. Tab Bar at the bottom, with 'My Claims' as the active tab, maintaining global navigation consistency. Each claim in the list is an inline tappable element.

### Linked Screens
- Home Screen
- Visual Claim Progress Timeline
- Select Claim Type
- Filter Claims (Modal)

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, Bold, 24pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- Active tab bar icon/label
- 'Start New Claim' button text (if outline) or background

**Accent Color:**
- Status indicators for active claims
- Small icons within list items

---

# Visual Claim Progress Timeline

### Purpose
To provide a detailed, interactive visual timeline of a specific claim's progress, showing current status, completed steps, and future actions.

### Primary Features
- Visual Claim Timeline
- Jargon Translator
- Partner Support Mode

### Navigation Elements
- **Title:** `Claim [Claim ID] Progress`
- **Components:**
  - Top App Bar
  - Inline Contextual Action
  - Top Right Action Button
  - Swipe Gesture
  - System Back Button

### Sections
- Your Claim Journey
- Next Steps

### Component Placement Rules
Top App Bar with a clear title (Claim ID) and a back button. A 'Share with Partner' button in the top-right, leveraging the Partner Support Mode feature. The Visual Claim Timeline is the central, interactive element, horizontal scrollable. Tapping on a timeline stage expands details inline or via a bottom sheet.

### Linked Screens
- Select Claim to View
- Select Helper & Set Permissions
- Jargon Translator Modal
- Expanded Stage Details (Bottom Sheet)

### Progressive Disclosure
**Yes**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- Back button icon
- Pulsing 'current stage' indicator
- Completed stage checkmarks

**Accent Color:**
- Estimated completion times
- Haptic feedback on stage completion
- 'Share with Partner' icon

---

# Select Helper & Set Permissions

### Purpose
To allow the primary user to invite a helper (partner) and define specific permissions for their access to the claim.

### Primary Features
- Partner Support Mode
- Guided Co-Browsing Support

### Navigation Elements
- **Title:** `Invite a Helper`
- **Components:**
  - Top App Bar
  - Modal Sheet
  - Inline Contextual Action
  - Top Right Action Button
  - Swipe Gesture
  - System Back Button

### Sections
- Invite a Contact
- Set Permissions

### Component Placement Rules
Presented as a modal sheet (full-screen) for a focused, temporary task, with a 'Cancel' button in the top-left, aligning with iOS modal patterns. Inline elements for contact selection and permission toggles. A prominent 'Send Invitation' button at the bottom.

### Linked Screens
- Visual Claim Progress Timeline
- Invitation Sent Confirmation (Toast/Alert)

### Progressive Disclosure
**No**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Modal title
- 'Send Invitation' button background
- Active toggle states

**Accent Color:**
- Toggle switches
- Subtle highlights on interactive elements

---

# Helper Accepts Invitation

### Purpose
To provide the invited helper (David) with a clear interface to accept the invitation and access the shared claim, with an option to activate 'Helper View'.

### Primary Features
- Partner Support Mode

### Navigation Elements
- **Title:** `Invitation from Emily`
- **Components:**
  - Top App Bar
  - Inline Contextual Action

### Sections
- You've been invited!
- Access Options

### Component Placement Rules
Top App Bar with a clear, personalized title ('Invitation from Emily'). A prominent 'Accept Invitation' button. An inline toggle for 'Activate Helper View' (Partner Support Mode).

### Linked Screens
- Helper Claim View (with Partner Support Mode active)

### Progressive Disclosure
**No**

### Text Styles
- **Title:** Montserrat, SemiBold, 20pt
- **Body:** Poppins, Regular, 16pt
- **CTA:** Poppins, SemiBold, 18pt

### Color Usage
**Primary Color:**
- Top App Bar title
- 'Accept Invitation' button background
- Active toggle state for Helper View

**Accent Color:**
- Toggle switch for Helper View
- Subtle highlights


Strictly follow the below mentioned color scheme for generating UI. Be consistent. 

Do not deviate.

Primary - "#A3C1DA"

Secondary - "#F6A3A3"

Background- "#F7F7F7"
</screen_specifications>
"""
}

response = requests.post("http://127.0.0.1:8000/generate-initial", json=payload)

print(response)