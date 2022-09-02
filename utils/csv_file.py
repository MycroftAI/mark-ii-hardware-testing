"""
csv file format
"""
csv_line_keys = [
    'serial_number',
    'version',
    'tester',
    'cpu',
    'memory',
    'storage',
    'touch_screen',
    'volume',
    'button_right',
    'button_left',
    'slider',
    'brightness',
    'recording',
    'touch_working',
    'camera',
    'bluetooth',
    'fan'
]
def write_test_results_to_file(csv_data):
    csv_line = ''
    for key in csv_line_keys:
        csv_line += str( csv_data.get(key,'ERR') ) + ','

    csv_line = csv_line[:-1]
    csv_line += '\n'
    #print(csv_line)
    with open('test_results.csv', 'a') as file_handle:
        file_handle.write(csv_line)

"""
csv_data = { 
    'serial_number':1,
    'version':2,
    'tester':3,
    'cpu':4,
    'memory':5,
    'storage':6,
    'touch_screen':7,
    'volume':8,
    'button_right':9,
    'button_left':10,
    'slider':11,
    'brightness':12,
    'recording':13,
    'touch_working':14,
    'camera':15,
    'bluetooth':16,
    'fan':17,
}

write_test_results_to_file(csv_data)
"""

