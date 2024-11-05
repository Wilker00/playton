# 1. Initialize Main Window and Canvas
#
# 2. Define Variables:
#    drag_data = {
#        "drag_hold": False,         # State of drag hold
#        "checkpoints": [],          # List to store checkpoints
#        "selected_item": None,      # The currently selected item to drag
#    }
#
# 3. Create a Toolbar/Menu with options, initially hidden
#
# 4. Define Function toggle_drag_hold(event):
#     - If drag_data["drag_hold"] is False:
#         - Set drag_data["drag_hold"] to True
#         - Show the toolbar with options
#     - Else:
#         - Set drag_data["drag_hold"] to False
#         - Hide the toolbar
#
# 5. Define Function add_checkpoint(event):
#     - If drag_data["drag_hold"] is True:
#         - Get event coordinates (x, y)
#         - Create a checkpoint (e.g., small circle) at (x, y)
#         - Add (x, y) to drag_data["checkpoints"]
#
# 6. Define Function start_drag(event):
#     - If drag_data["drag_hold"] is True:
#         - Set drag_data["selected_item"] to the item closest to event coordinates
#         - Save initial click coordinates
#
# 7. Define Function drag(event):
#     - If drag_data["selected_item"] is set:
#         - Calculate movement offset from initial coordinates
#         - Move drag_data["selected_item"] by the offset
#
# 8. Define Function stop_drag(event):
#     - Clear drag_data["selected_item"]
#
# 9. Bind Mouse Events:
#    - Right-Click to toggle_drag_hold or add_checkpoint
#    - Left-Click to start_drag
#    - Mouse Motion to drag
#    - Mouse Release to stop_drag
