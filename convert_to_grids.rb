require 'fastest-csv'
require 'csv'
require 'json'

def get_grids(file_name)
  CSV.foreach("#{file_name}", headers: true) do |row|
    grid = eval(row['boundingBox'])
    puts row['downloadURL']
    puts grid
  end

end

def process_csv_to_grid(file_name)
  x = 0
  FastestCSV.foreach("#{file_name}") do |row|
    state_code = file_name.split("_")[1].split("/")[-1],
    #county_name = file_name.split("_")[2..-2].join("_"),
    #county_code = file_name.split("_")[-1].split(".")[0]

    lat = row[4].to_f.floor
    lng = row[5].to_f.floor * (-1)
    CSV.open("n#{lat}w#{lng}.csv","a") do |csv|
      row << state_code
      csv << row
      x += 1
      print "#{x} \r"
    end
    #sleep 10

  end
end


#get_grids("master_list_ned_img.csv")
puts process_csv_to_grid("nytest_result.csv")
