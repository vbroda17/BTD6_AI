class DesktopNotVisibleException(Exception):
    """Exception raised when the desktop is not visible."""
    def __init__(self, message="Desktop is not visible."):
        super().__init__(message)

class TemplateMatchException(Exception):
    """
    Exception raised when a screen does not match the given template.
    """
    def __init__(self, template_path, confidence, threshold):
        self.template_path = template_path
        self.confidence = confidence
        self.threshold = threshold
        super().__init__(f"Template match failed for: {template_path}. "
                         f"Confidence: {confidence:.2f}, Threshold: {threshold:.2f}")

class ButtonNotFoundException(Exception):
    """
    Exception raised when a button cannot be found on the screen.
    """
    def __init__(self, template_path, confidence):
        self.template_path = template_path
        self.confidence = confidence
        super().__init__(f"Button not found for template: {template_path}. Confidence: {confidence:.2f}")

class GameLaunchTimeoutException(Exception):
    """
    Exception raised when the game start screen does not appear within the expected time frame.
    """
    def __init__(self, message="Game start screen did not appear within the timeout period."):
        super().__init__(message)


