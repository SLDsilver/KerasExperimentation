%Resolve prior variables 
function toFile(fname)
    %Run the function
    answer = read_complex_binary(fname);

    %Write to another file
    fileID = fopen(strrep(fname,'.dat','.txt'), 'wt');
    
    i = 1;
    while(1)
        try
            fprintf(fileID, '%f\n', answer(i)); 
            fprintf(fileID, '%f\n', answer(i)/1i);
            i = i+1;
        catch
            break;
        end
    end
    fclose(fileID);
end

