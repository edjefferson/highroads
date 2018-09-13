require 'csv'
require 'zip'
require 'active_record'
require 'rgeo/shapefile'


def import_states
  states = {}
  CSV.foreach("state_codes.csv", headers: true) do |row|
    states[row[0]] = row[1]
  end
  states
end

def import_counties
  counties = {}
  CSV.foreach("state_codes.csv", headers: true) do |row|
    counties[row[0]] = [row[1],row[2],row[3]]
  end
  counties
end

def download_roads(states)
  states.each do |k,v|
    url = "https://www2.census.gov/geo/tiger/TIGER2017/PRISECROADS/tl_2017_#{v}_prisecroads.zip"

    system("curl -o roads/#{v}_#{k.gsub(" ","_")}.zip #{url}")
  end
end

def download_all_roads(counties)
  counties.each do |k,v|
    url = "https://www2.census.gov/geo/tiger/TIGER2017/ROADS/#{k}"
    system("curl -o all_roads/#{v[2]}_#{v[1].gsub(" ","_")}_#{v[0]}.zip #{url}")
  end
end


def shapefile_to_csv(input_file, output_file)
  RGeo::Shapefile::Reader.open(input_file) do |file|
    puts "File contains #{file.num_records} records."
    CSV.open(output_file, "w") do |csv|
      file.each do |record|
        print "#{record.index}\r"
        record.geometry.coordinates.each do |group|
          group.each do |coord_set|
            csv << [record.attributes["LINEARID"],record.attributes["FULLNAME"], record.attributes["RTTYP"], record.attributes["MTFCC"], coord_set[1],coord_set[0]]  #,get_elevation_in_meters(coord_set[1],coord_set[0])]
          end
        end
      end
    end
  end
end

def counties_to_csv
  zips = Dir["all_roads/*.zip"].sort
  counties = zips.map do |zip|
    {
      state_code: zip.split("_")[1].split("/")[-1],
      county_name: zip.split("_")[2..-2].join(" "),
      county_code: zip.split("_")[-1]
    }
  end

  counties.each do |county|
    puts county.inspect
    Zip::File.open("all_roads/#{county[:state_code]}_#{county[:county_name]}_#{county[:county_code]}") { |zip_file|
       zip_file.each { |f|
         f_path=File.join("temp_dir", f.name)
         FileUtils.mkdir_p(File.dirname(f_path))
         zip_file.extract(f, f_path) unless File.exist?(f_path)
       }
    }
    puts "zip extracted"
    file = Dir.glob("temp_dir/*.shp")[0]
    shapefile_to_csv(file, "all_roads_csvs/#{county[:state_code]}_#{county[:county_name]}_#{county[:county_code]}.csv")
    FileUtils.rm_rf('temp_dir')
    puts "temp files deleted"
  end
end



def database_import
end

#download_roads(import_states)
#download_all_roads(import_counties)
#states_to_csv(import_states)
counties_to_csv
