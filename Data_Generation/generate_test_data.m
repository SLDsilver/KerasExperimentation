%This is a script file meant to automate the test data generation process
function generate_test_data(numTrain,numTests)
    generate_files('samples',numTrain);
    generate_files('tests',numTests);
end

function generate_files(dirname, numFiles)
    file_count = numFiles;
    commandStr = ['rm -r ' dirname '; mkdir ' dirname '; cd ' dirname '; python ' pwd '/GenIQ.py ' numFiles];
    [status] = system(commandStr);
    if status==0 %If the python script properly executed
        fprintf('.dat files generated properly \n');
    end
       for i = 0:(int32(str2double(file_count))-1)
            file_name = [dirname '/samples' num2str(i) '.dat'];
            fprintf(['converting: ' file_name '\n'])
            toFile(file_name);
            system(['rm ' file_name]);
       end
    fprintf('Complete \n')
    system('cd ..');
end
