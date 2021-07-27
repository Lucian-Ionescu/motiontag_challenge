from motiontag_challenge.request import send_request, load_base_data
import sys

# if __name__ == '__main__':
data = None
# if len(sys.argv) > 1:
#     file = sys.argv[1]
#     data = load_base_data()

data_api = send_request(
    data=data,             # if none, data is loaded from file before sent to API
    use_model=True,        # switch: use ML model or thresholding
    include_labels=False,  # whether to send labels for evaluation
    verbose=False)         # server verbose mode for testing

print(data_api)
