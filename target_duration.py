# First start CASA then run
import numpy as np

ms.open(input('Enter ms name within \' \': '))

scan_summary = ms.getscansummary()
target_scan_list = scan_summary.keys()
target_scan_list = list(map(int, target_scan_list))
durations = []
old_spws = []
old_field = ''
for kk in range(len(target_scan_list)):
    ii = target_scan_list[kk]

    try:
        end_time = scan_summary[str(ii)]['0']['EndTime']
        begin_time = scan_summary[str(ii)]['0']['BeginTime']
        new_spws = scan_summary[str(ii)]['0']['SpwIds']
        new_field = scan_summary[str(ii)]['0']['FieldId']

        if ((kk > 0) and (target_scan_list[kk-1] == ii-1) and (set(new_spws) == set(old_spws)) and (new_field == old_field)):
        # if contiguous scans, just increase the time on the previous one
            durations[-1] = 86400*(end_time - old_begin_time)
        else:
            durations.append(86400*(end_time - begin_time))
            old_begin_time = begin_time
        old_spws = new_spws
        old_field = new_field

    except KeyError:
        print("Warning: scan "+str(ii)+" is completely flagged and missing from calibrators.ms")

ms.close()

print('Total time: '+ str(int(np.sum(durations)/60.0)) + ' min')
