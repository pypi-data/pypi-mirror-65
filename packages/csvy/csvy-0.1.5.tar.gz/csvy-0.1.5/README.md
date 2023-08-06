csvy
----

Basic context wrappers for stardard library csv.read and csv.write methods.

##### Writer Example
B

The writer returns a straight up csv.writer object:

    import csvy

    with csvy.writer('csvpath.csv') as csvfile:
        csvfile.writerow([1, 2, 3, 4])


##### Reader Example

The reader returns a proxy object that behaves a bit differently. You must
call the `iter` method that yield an enumerator:

    import csvy

    with csvy.reader('csvpath.csv') as csvfile:
        for index, row in csvfile.iter():
            print(f"{index}: {row}")


If a header row is detected, the row object will be a `namedtuple` based
on the values of the header line:

    """
    src.csv:

    A,B,C,column D
    1,2,3,4
    5,6,7,8

    """
    import csvy

    with csvy.reader('src.csv') as csvfile:
        for index, row in csvfile.iter():
            print(row.a)
            print(row.column_d)


