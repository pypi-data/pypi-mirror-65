#include <pybind11/pybind11.h>
#include <exiv2/exiv2.hpp>
#include <string>
#include <sstream>
#include <iostream>

namespace py = pybind11;
const std::string COMMA = ", ";
const char *EXCEPTION_HINT = "Caught Exiv2 exception: ";
std::stringstream error_log;

#define catch_block                       \
    catch (std::exception & e)            \
    {                                     \
        std::stringstream ss;             \
        ss << EXCEPTION_HINT << e.what(); \
        return py::str(ss.str());         \
    }

#define read_block                                                     \
    {                                                                  \
        py::list table;                                                \
        for (; i != end; ++i)                                          \
        {                                                              \
            py::list line;                                             \
            line.append(py::bytes(i->key()));                          \
                                                                       \
            std::stringstream _value;                                  \
            _value << i->value();                                      \
            line.append(py::bytes(_value.str()));                      \
                                                                       \
            const char *typeName = i->typeName();                      \
            line.append(py::bytes((typeName ? typeName : "Unknown"))); \
            table.append(line);                                        \
        }                                                              \
        return table;                                                  \
    }

void logHandler(int level, const char *msg)
{
    switch (level)
    {
    case Exiv2::LogMsg::debug:
    case Exiv2::LogMsg::info:
    case Exiv2::LogMsg::warn:
        std::cout << msg << std::endl;
        break;

    case Exiv2::LogMsg::error:
        // For unknown reasons, the exception thrown here cannot be caught, so save the log to error_log
        // throw std::exception(msg);
        error_log << msg;
        break;

    default:
        return;
    }
}

void check_error_log()
{
    std::string str = error_log.str();
    if(str != ""){
        error_log.clear();  // Clear it so it can be used again
        error_log.str("");
        throw std::runtime_error(str);
    }
}

void set_log_level(int level)
{
    if (level == 0)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::debug);
    if (level == 1)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::info);
    if (level == 2)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::warn);
    if (level == 3)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::error);
    if (level == 4)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::mute);
}

void init()
{
    Exiv2::LogMsg::setHandler(logHandler);
}

py::object open_image(const char *filename)
{
    Exiv2::Image::AutoPtr *img = new Exiv2::Image::AutoPtr;
    *img = Exiv2::ImageFactory::open(filename);
    if (img->get() == 0)
        throw Exiv2::Error(Exiv2::kerErrorMessage, "Can not open this file.");
    (*img)->readMetadata();
    check_error_log();
    return py::cast(img);
}

void close_image(Exiv2::Image::AutoPtr *img)
{
    delete img;
    check_error_log();
}

py::object read_exif(Exiv2::Image::AutoPtr *img)
{
    Exiv2::ExifData &data = (*img)->exifData();
    Exiv2::ExifData::iterator i = data.begin();
    Exiv2::ExifData::iterator end = data.end();
    read_block;
    check_error_log();
}

py::object read_iptc(Exiv2::Image::AutoPtr *img)
{
	Exiv2::IptcData &data = (*img)->iptcData();
	Exiv2::IptcData::iterator i = data.begin();
	Exiv2::IptcData::iterator end = data.end();
	read_block;
    check_error_log();
}

py::object read_xmp(Exiv2::Image::AutoPtr *img)
{
	Exiv2::XmpData &data = (*img)->xmpData();
	Exiv2::XmpData::iterator i = data.begin();
	Exiv2::XmpData::iterator end = data.end();
	read_block;
    check_error_log();
}

py::object read_raw_xmp(Exiv2::Image::AutoPtr *img)
{
    check_error_log();
	return py::bytes((*img)->xmpPacket());
}

void modify_exif(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::ExifData &exifData = (*img)->exifData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);          // can't use item[0] here, so convert to py::list
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));

        Exiv2::ExifData::iterator key_pos = exifData.findKey(Exiv2::ExifKey(key));
		if (key_pos != exifData.end())
			exifData.erase(key_pos);    // delete the existing tag to write a value
		if (value == "")
			continue;                   // skip the tag if value == ""
		exifData[key] = value;          // write a value to the tag
	}
	(*img)->setExifData(exifData);
	(*img)->writeMetadata();
    check_error_log();
}

void modify_iptc(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::IptcData &iptcData = (*img)->iptcData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));
        std::string typeName = py::bytes(line[2].attr("encode")(encoding));

        Exiv2::IptcData::iterator key_pos = iptcData.findKey(Exiv2::IptcKey(key));
		while (key_pos != iptcData.end()){  // use the while loop because the iptc key may repeat
			iptcData.erase(key_pos);
            key_pos = iptcData.findKey(Exiv2::IptcKey(key));
        }
		if (value == "")
			continue;

        if (typeName == "array")
		{
            Exiv2::Value::AutoPtr exiv2_value = Exiv2::Value::create(Exiv2::string);
            int pos = 0;
			int COMMA_pos = 0;
			while (COMMA_pos != std::string::npos)
			{
				COMMA_pos = value.find(COMMA, pos);
                exiv2_value->read(value.substr(pos, COMMA_pos - pos));
                iptcData.add(Exiv2::IptcKey(key), exiv2_value.get());
				pos = COMMA_pos + COMMA.length();
			}
        }
        else
            iptcData[key] = value;
	}
	(*img)->setIptcData(iptcData);
	(*img)->writeMetadata();
    check_error_log();
}

void modify_xmp(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::XmpData &xmpData = (*img)->xmpData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));
        std::string typeName = py::bytes(line[2].attr("encode")(encoding));
        
        Exiv2::XmpData::iterator key_pos = xmpData.findKey(Exiv2::XmpKey(key));
		if (key_pos != xmpData.end())
			xmpData.erase(key_pos);
		if (value == "")
			continue;

        if (typeName == "array")
		{
            int pos = 0;
			int COMMA_pos = 0;
			while (COMMA_pos != std::string::npos)
			{
				COMMA_pos = value.find(COMMA, pos);
				xmpData[key] = value.substr(pos, COMMA_pos - pos);
				pos = COMMA_pos + COMMA.length();
			}
        }
        else
            xmpData[key] = value;
    }
	(*img)->setXmpData(xmpData);
	(*img)->writeMetadata();
    check_error_log();
}

void clear_exif(Exiv2::Image::AutoPtr *img)
{
	Exiv2::ExifData exifData; // create an empty container of exif metadata
	(*img)->setExifData(exifData);
	(*img)->writeMetadata();
    check_error_log();
}

void clear_iptc(Exiv2::Image::AutoPtr *img)
{
	Exiv2::IptcData iptcData;
	(*img)->setIptcData(iptcData);
	(*img)->writeMetadata();
    check_error_log();
}

void clear_xmp(Exiv2::Image::AutoPtr *img)
{
	Exiv2::XmpData xmpData;
	(*img)->setXmpData(xmpData);
	(*img)->writeMetadata();
    check_error_log();
}

PYBIND11_MODULE(exiv2api, m)
{
    m.doc() = "Expose the API of exiv2 to Python.";
    py::class_<Exiv2::Image::AutoPtr>(m, "Exiv2_Image_AutoPtr")
        .def(py::init<>());
    m.def("set_log_level", &set_log_level);
    m.def("init", &init);
    m.def("open_image", &open_image);
    m.def("close_image", &close_image);
    m.def("read_exif", &read_exif);
    m.def("read_iptc", &read_iptc);
    m.def("read_xmp", &read_xmp);
    m.def("read_raw_xmp", &read_raw_xmp);
    m.def("modify_exif", &modify_exif);
    m.def("modify_iptc", &modify_iptc);
    m.def("modify_xmp", &modify_xmp);
    m.def("clear_exif", &clear_exif);
    m.def("clear_iptc", &clear_iptc);
    m.def("clear_xmp", &clear_xmp);
}
