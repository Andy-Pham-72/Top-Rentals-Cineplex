import csv

def save_rentals_to_csv_file(rentals_list, file_name):
    """
    function to write csv "rentals" variable to csv file
    
    :param rentals_list: list
                A list of the top rental movies from Cineplex
    :param file_name: str
                A string of the directory path which is used to save the csv file
    :return:

    """
    with open(file_name, 'w') as csvfile:
        fieldnames = ['title', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for rental in rentals_list:
            
            writer.writerow({'title' : rental.title, 'year' : int(rental.year)})
            