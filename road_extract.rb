require 'rgeo/shapefile'
require 'csv'

def shapefile_to_csv(input_file, output_file)
  RGeo::Shapefile::Reader.open(input_file) do |file|
    puts "File contains #{file.num_records} records."
    CSV.open(output_file, "w") do |csv|
      file.each do |record|
        print "#{record.index}\r"
        if record.geometry.coordinates.count > 1
          puts record.inspect
          puts record.geometry.coordinates.count
          puts "FART"
          sleep 5
          break
        end
        record.geometry.coordinates[0].each do |coord_set|
          csv << [record.attributes["LINEARID"],record.attributes["FULLNAME"], record.attributes["RTTYP"], record.attributes["MTFCC"], coord_set[1],coord_set[0]]  #,get_elevation_in_meters(coord_set[1],coord_set[0])]
        end
      end
    end
  end
end

#shapefile_to_csv('tl_2017_us_primaryroads/tl_2017_us_primaryroads.shp',"2017primaryroads.csv")
shapefile_to_csv('NY_New_York_36061/tl_2017_36061_roads.shp',"nytest.csv")
