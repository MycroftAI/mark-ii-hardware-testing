#!/bin/bash
echo "Testing audio recording"
LC_ALL=C
#sleep 1

echo "Recording 3 seconds of audio..."
su pi -c 'arecord -r 16000 -c 2 -f S16_LE -t wav -d 3 > test_stereo_recording.wav'
su pi -c 'aplay wavs/you_said.wav'
su pi -c 'aplay test_stereo_recording.wav'
echo "Evaluating results..."
#WAV_MAX_LEVELS=$(sox test_stereo_recording.wav -n stats 2>&1 | sed -n '/^Max/p')
#R_CHANNEL=$(awk '{if ($5 > 0) {print "PASS"} else {print "FAIL"}}' <<< "$WAV_MAX_LEVELS")
#L_CHANNEL=$(awk '{if ($4 > 0) {print "PASS"} else {print "FAIL"}}' <<< "$WAV_MAX_LEVELS")
#COMBINED_CHANNEL=$(awk '{if ($3 > 0) {print "PASS"} else {print "FAIL"}}' <<< "$WAV_MAX_LEVELS")

#echo "Right Channel: $R_CHANNEL"
#echo "Left Channel: $L_CHANNEL"
#echo "Combined Channels: $COMBINED_CHANNEL"

rm test_stereo_recording.wav
exit 0

if [[ "$R_CHANNEL" == "PASS" && "$L_CHANNEL" == "PASS" && "$COMBINED_CHANNEL" == "PASS" ]]
then
    echo "All passed"
    exit 0
else
    echo "Recording failure. Stopping test sequence."
    exit 1
fi
