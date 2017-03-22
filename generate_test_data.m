%This is a script file meant to automate the test data generation process
function generate_test_data(numFiles)
    file_count = numFiles;
    commandStr = ['rm -r samples/; mkdir samples; cd samples; python ' pwd '/GenIQ.py ' numFiles];
    [status] = system(commandStr);
    if status==0 %If the python script properly executed
        fprintf('command executed properly');
    end
    
    for i = 0:(int32(str2double(file_count))-1)
        file_name = ['samples/samples' num2str(i) '.dat'];
        fprintf(['\n converting: ' file_name])
        toFile(file_name);
        system(['rm ' file_name]);
    end
    
    system('cd ..');

end
