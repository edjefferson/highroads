require 'zip'
require 'csv'
require 'open-uri'
require 'curb'
require 'ffi-gdal'
require 'ogr'
require 'gdal'
require 'active_record'

ActiveRecord::Base.establish_connection(
  :adapter  => 'postgresql',
  :database => 'highroads',
  :host     => 'localhost'
)


class RoadSegment < ActiveRecord::Base
end

def grid_scan(list_of_squares)
  CSV.foreach(list_of_squares, :headers => true) do |row|
    url = row["downloadURL"]
    boundingBox = {}
    row["boundingBox"][1..-2].split(",").each do |x|
      boundingBox[x.split(":")[0].to_sym] = x.split(":")[1].to_f
    end
    #puts boundingBox
    road_segments =  RoadSegment.where(:elevation => nil, :lng => boundingBox[:minX]..boundingBox[:maxX], :lat => boundingBox[:minY]..boundingBox[:maxY])
    if road_segments.count > 0
      puts "#{road_segments.count} roads segments needing data"
      extract_img_data(url)
      begin
        elevation_array = get_elevation_array
      rescue
        retry
      end
      road_segments.each do |road|
        elevation =  get_elevation_in_meters(elevation_array, road["lat"], road["lng"], boundingBox)
        road.update(elevation: elevation)
        puts elevation
      end
    end
  end
end

def extract_img_data(url)
  system("curl -o output.zip #{url}")
  Zip::File.open("output.zip") { |zip_file|
     zip_file.each { |f|
     f_path=File.join("temp_dir", f.name)
     FileUtils.mkdir_p(File.dirname(f_path))
     zip_file.extract(f, f_path) unless File.exist?(f_path)
   }
  }
  puts "zip extracted"
  file = Dir.glob("temp_dir/*.img")
  FileUtils.cp(file[0],"output.img")
  puts "img extracted"
  FileUtils.rm_rf('temp_dir')
  puts "temp files deleted"
end


def get_elevation_array
  obj = GDAL::Dataset.open("output.img","r")
  array = []
  obj.raster_band(1).readlines.each {|line| array << line}
  puts "array extracted"
  array
end

def get_elevation_in_meters(elevation_array, lat, lng, boundingBox)
  y_range = boundingBox[:maxY] - boundingBox[:minY]
  y_stop_length = y_range/elevation_array.count
  y_diff = boundingBox[:maxY] - lat
  y_stops = y_diff/y_stop_length

  x_range = boundingBox[:maxX] - boundingBox[:minX]
  x_stop_length = x_range/elevation_array.count
  x_diff = lng - boundingBox[:minX]
  x_stops = x_diff/x_stop_length
  elevation_array[y_stops.to_i][x_stops.to_i]
end

grid_scan('master_list_ned_img.csv')


#extract_img_data("https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/IMG/USGS_NED_13_n30w101_IMG.zip")
