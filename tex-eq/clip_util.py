# ref: https://gist.github.com/XuankangLin/7ec82f80a0044a52330720244de2d15a
from Foundation import NSData
from AppKit import NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboard
from io import BytesIO

# pip install -U PyObjC
# https://github.com/RhetTbull/textinator/blob/main/src/pasteboard.py
# https://stackoverflow.com/questions/54008175/copy-an-image-to-macos-clipboard-using-python

def copy_plt_to_clipboard(fig):
    # Save the figure to a BytesIO buffer in PNG format
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    buffer.seek(0)  # Reset buffer pointer to the beginning

    # Convert the BytesIO buffer to NSData
    png_data = NSData.dataWithBytes_length_(buffer.getvalue(), len(buffer.getvalue()))

    # Get the general pasteboard
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.clearContents()  # Clear existing content on the pasteboard

    # Set the PNG data to the pasteboard
    pasteboard.setData_forType_(png_data, NSPasteboardTypePNG)

    print("Figure copied to clipboard as PNG!")