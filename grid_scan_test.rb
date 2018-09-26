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





def extract_img_data(image_file)
  puts image_file
  Zip::File.open(image_file) { |zip_file|
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
  puts array.count
  array
end

def get_elevation_in_meters(elevation_array, lat, lng, boundingBox)
  puts boundingBox
  puts lat
  puts lng
  y_range = boundingBox[:maxY] - boundingBox[:minY]
  y_stop_length = y_range/elevation_array.count
  #puts boundingBox[:maxY]
  y_diff = boundingBox[:maxY] - (lat)
  #puts y_diff
  y_stops = y_diff/y_stop_length

  x_range = boundingBox[:maxX] - boundingBox[:minX]
  x_stop_length = x_range/elevation_array.count
  x_diff = lng - boundingBox[:minX]
  x_stops = x_diff/x_stop_length
  elevation_array[y_stops.to_i][x_stops.to_i]
end

#grid_scan('master_list_ned_img.csv')


#extract_img_data("https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/IMG/USGS_NED_13_n30w101_IMG.zip")
bounding_box_string = "{minY:32.99944444444,minX:-85.00055555556,maxY:34.00055555556,maxX:-83.99944444444}"

image_file = "testing/n33w085.zip"
road_file = "testing/n33w085.csv"


boundingBox = {}
bounding_box_string[1..-2].split(",").each do |x|
  boundingBox[x.split(":")[0].to_sym] = x.split(":")[1].to_f
end
road_segments = []
#extract_img_data(image_file)
#begin

elevation_array = get_elevation_array
#rescue
#  retry
#end
CSV.foreach(road_file) do |road|


  #puts road.inspect
  elevation =  get_elevation_in_meters(elevation_array, road[5].to_f, road[6].to_f, boundingBox)
  #puts elevation


end
