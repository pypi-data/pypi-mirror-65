function I = xarrayind2vector(V, key)

C = cell(V.indexes{key}.values.tolist);  % might be numeric or cell array of strings

if iscellstr(C) || (length(C) > 1 && isa(C{1}, 'py.str'))
    I = cellfun(@char, C, 'uniformoutput', false);
elseif isa(C{1}, 'py.datetime.datetime')
    I = char(C{1}.isoformat());
elseif isa(C{1}, 'py.int') && C{1} > 1e12
    C = cellfun(@double,C)/1e9;
    I = datetime(C, 'convertfrom','posixtime');
else
    I = cell2mat(C);
end % if

end % function