class DesktopNotVisibleException(Exception):
  """Exception raised when the desktop is not visible."""
  def __init__(self, message="Desktop is not visible."):
    super().__init__(message)

class ClickException(Exception):
  """Exception raised when a click does not work due to the providerd immage."""
  def __init__(self, template_path, confidence, threshold):
    self.template_path = template_path
    self.confidence = confidence
    self.threshold = threshold
    super().__init__(f"Template match failed for: {template_path}. "
                      f"Confidence: {confidence:.2f}, Threshold: {threshold:.2f}")
    
class TimeoutException(Exception):
  """Exception raised because of a timeout. May need to adjust time waits."""
  def __init__(self, elapsed_time, operation_detail="Operation timed out"):
    self.elapsed_time = elapsed_time
    self.operation_detail = operation_detail
    super().__init__(f"Timeout occurred after {elapsed_time:.2f} seconds. {operation_detail}")
