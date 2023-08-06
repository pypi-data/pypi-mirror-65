#pragma once
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/connection.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/materialized_query_result.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/chunk_collection.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/order_type.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/constants.hpp
//
//
//===----------------------------------------------------------------------===//



#include <cstdlib>
#include <memory>
#include <string>
#include <vector>
#include <cmath>

namespace duckdb {

//! inline std directives that we use frequently
using std::move;
using std::string;
using std::unique_ptr;
using data_ptr = unique_ptr<char[]>;
using std::vector;

// NOTE: there is a copy of this in the Postgres' parser grammar (gram.y)
#define DEFAULT_SCHEMA "main"
#define TEMP_SCHEMA "temp"
#define INVALID_SCHEMA ""

//! The vector size used in the execution engine
#ifndef STANDARD_VECTOR_SIZE
#define STANDARD_VECTOR_SIZE 1024
#endif

#if ((STANDARD_VECTOR_SIZE & (STANDARD_VECTOR_SIZE - 1)) != 0)
#error Vector size should be a power of two
#endif

//! a saner size_t for loop indices etc
typedef uint64_t idx_t;

//! The type used for row identifiers
typedef int64_t row_t;

//! The type used for hashes
typedef uint64_t hash_t;

//! The value used to signify an invalid index entry
extern const idx_t INVALID_INDEX;

//! data pointers
typedef uint8_t data_t;
typedef data_t *data_ptr_t;
typedef const data_t *const_data_ptr_t;

//! Type used to represent dates
typedef int32_t date_t;
//! Type used to represent time
typedef int32_t dtime_t;
//! Type used to represent timestamps
typedef int64_t timestamp_t;
//! Type used for the selection vector
typedef uint16_t sel_t;
//! Type used for transaction timestamps
typedef idx_t transaction_t;

//! Type used for column identifiers
typedef idx_t column_t;
//! Special value used to signify the ROW ID of a table
extern const column_t COLUMN_IDENTIFIER_ROW_ID;

//! The maximum row identifier used in tables
extern const row_t MAX_ROW_ID;

//! Zero selection vector: completely filled with the value 0 [READ ONLY]
extern const sel_t ZERO_VECTOR[STANDARD_VECTOR_SIZE];

extern const transaction_t TRANSACTION_ID_START;
extern const transaction_t MAXIMUM_QUERY_ID;
extern const transaction_t NOT_DELETED_ID;

extern const double PI;

struct Storage {
	//! The size of a hard disk sector, only really needed for Direct IO
	constexpr static int SECTOR_SIZE = 4096;
	//! Block header size for blocks written to the storage
	constexpr static int BLOCK_HEADER_SIZE = sizeof(uint64_t);
	// Size of a memory slot managed by the StorageManager. This is the quantum of allocation for Blocks on DuckDB. We
	// default to 256KB. (1 << 18)
	constexpr static int BLOCK_ALLOC_SIZE = 262144;
	//! The actual memory space that is available within the blocks
	constexpr static int BLOCK_SIZE = BLOCK_ALLOC_SIZE - BLOCK_HEADER_SIZE;
	//! The size of the headers. This should be small and written more or less atomically by the hard disk. We default
	//! to the page size, which is 4KB. (1 << 12)
	constexpr static int FILE_HEADER_SIZE = 4096;
};

uint64_t NextPowerOfTwo(uint64_t v);

} // namespace duckdb


namespace duckdb {

enum class OrderType : uint8_t { INVALID = 0, ASCENDING = 1, DESCENDING = 2 };
}

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/data_chunk.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/common.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/helper.hpp
//
//
//===----------------------------------------------------------------------===//





#include <algorithm>
#include <limits>
#include <sstream>

#ifdef _MSC_VER
#define suint64_t int64_t
#endif

namespace duckdb {
#if !defined(_MSC_VER) && (__cplusplus < 201402L)
template <typename T, typename... Args> unique_ptr<T> make_unique(Args &&... args) {
	return unique_ptr<T>(new T(std::forward<Args>(args)...));
}
#else // Visual Studio has make_unique
using std::make_unique;
#endif
template <typename S, typename T, typename... Args> unique_ptr<S> make_unique_base(Args &&... args) {
	return unique_ptr<S>(new T(std::forward<Args>(args)...));
}

template <class T> inline bool in_bounds(int64_t value) {
	return value >= std::numeric_limits<T>::min() && value <= std::numeric_limits<T>::max();
}

template <typename T, typename S> unique_ptr<S> unique_ptr_cast(unique_ptr<T> src) {
	return unique_ptr<S>(static_cast<S *>(src.release()));
}

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/assert.hpp
//
//
//===----------------------------------------------------------------------===//



#include <assert.h>



#include <type_traits>

namespace duckdb {

class Serializer;
class Deserializer;

struct blob_t {
	data_ptr_t data;
	idx_t size;
};

struct string_t;

template <class T> using child_list_t = std::vector<std::pair<std::string, T>>;
template <class T> using buffer_ptr = std::shared_ptr<T>;

template <class T, typename... Args> buffer_ptr<T> make_buffer(Args &&... args) {
	return std::make_shared<T>(std::forward<Args>(args)...);
}

struct list_entry_t {
	list_entry_t() = default;
	list_entry_t(uint64_t offset, uint64_t length) : offset(offset), length(length) {
	}

	uint64_t offset;
	uint64_t length;
};

//===--------------------------------------------------------------------===//
// Internal Types
//===--------------------------------------------------------------------===//

// taken from arrow's type.h
enum class TypeId : uint8_t {
	/// A NULL type having no physical storage
	NA = 0,

	/// Boolean as 1 bit, LSB bit-packed ordering
	BOOL = 1,

	/// Unsigned 8-bit little-endian integer
	UINT8 = 2,

	/// Signed 8-bit little-endian integer
	INT8 = 3,

	/// Unsigned 16-bit little-endian integer
	UINT16 = 4,

	/// Signed 16-bit little-endian integer
	INT16 = 5,

	/// Unsigned 32-bit little-endian integer
	UINT32 = 6,

	/// Signed 32-bit little-endian integer
	INT32 = 7,

	/// Unsigned 64-bit little-endian integer
	UINT64 = 8,

	/// Signed 64-bit little-endian integer
	INT64 = 9,

	/// 2-byte floating point value
	HALF_FLOAT = 10,

	/// 4-byte floating point value
	FLOAT = 11,

	/// 8-byte floating point value
	DOUBLE = 12,

	/// UTF8 variable-length string as List<Char>
	STRING = 13,

	/// Variable-length bytes (no guarantee of UTF8-ness)
	BINARY = 14,

	/// Fixed-size binary. Each value occupies the same number of bytes
	FIXED_SIZE_BINARY = 15,

	/// int32_t days since the UNIX epoch
	DATE32 = 16,

	/// int64_t milliseconds since the UNIX epoch
	DATE64 = 17,

	/// Exact timestamp encoded with int64 since UNIX epoch
	/// Default unit millisecond
	TIMESTAMP = 18,

	/// Time as signed 32-bit integer, representing either seconds or
	/// milliseconds since midnight
	TIME32 = 19,

	/// Time as signed 64-bit integer, representing either microseconds or
	/// nanoseconds since midnight
	TIME64 = 20,

	/// YEAR_MONTH or DAY_TIME interval in SQL style
	INTERVAL = 21,

	/// Precision- and scale-based decimal type. Storage type depends on the
	/// parameters.
	DECIMAL = 22,

	/// A list of some logical data type
	LIST = 23,

	/// Struct of logical types
	STRUCT = 24,

	/// Unions of logical types
	UNION = 25,

	/// Dictionary-encoded type, also called "categorical" or "factor"
	/// in other programming languages. Holds the dictionary value
	/// type but not the dictionary itself, which is part of the
	/// ArrayData struct
	DICTIONARY = 26,

	/// Map, a repeated struct logical type
	MAP = 27,

	/// Custom data type, implemented by user
	EXTENSION = 28,

	/// Fixed size list of some logical type
	FIXED_SIZE_LIST = 29,

	/// Measure of elapsed time in either seconds, milliseconds, microseconds
	/// or nanoseconds.
	DURATION = 30,

	/// Like STRING, but with 64-bit offsets
	LARGE_STRING = 31,

	/// Like BINARY, but with 64-bit offsets
	LARGE_BINARY = 32,

	/// Like LIST, but with 64-bit offsets
	LARGE_LIST = 33,

	// DuckDB Extensions
	VARCHAR = 200, // our own string representation, different from STRING and LARGE_STRING above
	VARBINARY = 201,
	POINTER = 202,
	HASH = 203,

	INVALID = 255
};

//===--------------------------------------------------------------------===//
// SQL Types
//===--------------------------------------------------------------------===//
enum class SQLTypeId : uint8_t {
	INVALID = 0,
	SQLNULL = 1, /* NULL type, used for constant NULL */
	UNKNOWN = 2, /* unknown type, used for parameter expressions */
	ANY = 3,     /* ANY type, used for functions that accept any type as parameter */

	BOOLEAN = 10,
	TINYINT = 11,
	SMALLINT = 12,
	INTEGER = 13,
	BIGINT = 14,
	DATE = 15,
	TIME = 16,
	TIMESTAMP = 17,
	FLOAT = 18,
	DOUBLE = 19,
	DECIMAL = 20,
	CHAR = 21,
	VARCHAR = 22,
	VARBINARY = 23,

	STRUCT = 100,
	LIST = 101
};

struct SQLType {
	SQLTypeId id;
	uint16_t width;
	uint8_t scale;

	// TODO serialize this
	child_list_t<SQLType> child_type;

	SQLType(SQLTypeId id = SQLTypeId::INVALID, uint16_t width = 0, uint8_t scale = 0)
	    : id(id), width(width), scale(scale) {
	}

	bool operator==(const SQLType &rhs) const {
		return id == rhs.id && width == rhs.width && scale == rhs.scale;
	}
	bool operator!=(const SQLType &rhs) const {
		return !(*this == rhs);
	}

	//! Serializes a SQLType to a stand-alone binary blob
	void Serialize(Serializer &serializer);
	//! Deserializes a blob back into an SQLType
	static SQLType Deserialize(Deserializer &source);

	bool IsIntegral() const;
	bool IsNumeric() const;

public:
	static const SQLType SQLNULL;
	static const SQLType BOOLEAN;
	static const SQLType TINYINT;
	static const SQLType SMALLINT;
	static const SQLType INTEGER;
	static const SQLType BIGINT;
	static const SQLType FLOAT;
	static const SQLType DOUBLE;
	static const SQLType DATE;
	static const SQLType TIMESTAMP;
	static const SQLType TIME;
	static const SQLType VARCHAR;
	static const SQLType STRUCT;
	static const SQLType LIST;
	static const SQLType ANY;

	//! A list of all NUMERIC types (integral and floating point types)
	static const vector<SQLType> NUMERIC;
	//! A list of all INTEGRAL types
	static const vector<SQLType> INTEGRAL;
	//! A list of ALL SQL types
	static const vector<SQLType> ALL_TYPES;
};

string SQLTypeIdToString(SQLTypeId type);
string SQLTypeToString(SQLType type);

SQLType MaxSQLType(SQLType left, SQLType right);
SQLType TransformStringToSQLType(string str);

//! Gets the internal type associated with the given SQL type
TypeId GetInternalType(SQLType type);
//! Returns the "simplest" SQL type corresponding to the given type id (e.g. TypeId::INT32 -> SQLTypeId::INTEGER)
SQLType SQLTypeFromInternalType(TypeId type);

//! Returns the TypeId for the given type
template <class T> TypeId GetTypeId() {
	if (std::is_same<T, bool>()) {
		return TypeId::BOOL;
	} else if (std::is_same<T, int8_t>()) {
		return TypeId::INT8;
	} else if (std::is_same<T, int16_t>()) {
		return TypeId::INT16;
	} else if (std::is_same<T, int32_t>()) {
		return TypeId::INT32;
	} else if (std::is_same<T, int64_t>()) {
		return TypeId::INT64;
	} else if (std::is_same<T, uint64_t>()) {
		return TypeId::HASH;
	} else if (std::is_same<T, uintptr_t>()) {
		return TypeId::POINTER;
	} else if (std::is_same<T, double>()) {
		return TypeId::DOUBLE;
	} else if (std::is_same<T, const char *>() || std::is_same<T, char *>()) {
		return TypeId::VARCHAR;
	} else {
		return TypeId::INVALID;
	}
}

template <class T> bool IsValidType() {
	return GetTypeId<T>() != TypeId::INVALID;
}

//! The TypeId used by the row identifiers column
extern const TypeId ROW_TYPE;

string TypeIdToString(TypeId type);
idx_t GetTypeIdSize(TypeId type);
bool TypeIsConstantSize(TypeId type);
bool TypeIsIntegral(TypeId type);
bool TypeIsNumeric(TypeId type);
bool TypeIsInteger(TypeId type);

template <class T> bool IsIntegerType() {
	return TypeIsIntegral(GetTypeId<T>());
}

bool ApproxEqual(float l, float r);
bool ApproxEqual(double l, double r);

}; // namespace duckdb


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/vector.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/bitset.hpp
//
//
//===----------------------------------------------------------------------===//



#include <bitset>

namespace duckdb {
using std::bitset;
}


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/selection_vector.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/unordered_map.hpp
//
//
//===----------------------------------------------------------------------===//



#include <unordered_map>

namespace duckdb {
using std::unordered_map;
}


namespace duckdb {
class VectorBuffer;

struct SelectionData {
	SelectionData(idx_t count) {
		owned_data = unique_ptr<sel_t[]>(new sel_t[count]);
		;
	}

	unique_ptr<sel_t[]> owned_data;
};

struct SelectionVector {
	SelectionVector() : sel_vector(nullptr) {
	}
	SelectionVector(sel_t *sel) {
		Initialize(sel);
	}
	SelectionVector(idx_t count) {
		Initialize(count);
	}
	SelectionVector(const SelectionVector &sel_vector) {
		Initialize(sel_vector);
	}
	SelectionVector(buffer_ptr<SelectionData> data) {
		Initialize(move(data));
	}

public:
	void Initialize(sel_t *sel) {
		selection_data.reset();
		sel_vector = sel;
	}
	void Initialize(idx_t count = STANDARD_VECTOR_SIZE) {
		selection_data = make_buffer<SelectionData>(count);
		sel_vector = selection_data->owned_data.get();
	}
	void Initialize(buffer_ptr<SelectionData> data) {
		selection_data = move(data);
		sel_vector = selection_data->owned_data.get();
	}
	void Initialize(const SelectionVector &other) {
		selection_data = other.selection_data;
		sel_vector = other.sel_vector;
	}

	bool empty() const {
		return !sel_vector;
	}
	void set_index(idx_t idx, idx_t loc) {
		sel_vector[idx] = loc;
	}
	void swap(idx_t i, idx_t j) {
		sel_t tmp = sel_vector[i];
		sel_vector[i] = sel_vector[j];
		sel_vector[j] = tmp;
	}
	idx_t get_index(idx_t idx) const {
		return sel_vector[idx];
	}
	sel_t *data() {
		return sel_vector;
	}
	buffer_ptr<SelectionData> sel_data() {
		return selection_data;
	}
	buffer_ptr<SelectionData> Slice(const SelectionVector &sel, idx_t count);

	string ToString(idx_t count = 0) const;
	void Print(idx_t count = 0) const;

private:
	sel_t *sel_vector;
	buffer_ptr<SelectionData> selection_data;
};

typedef unordered_map<sel_t *, buffer_ptr<VectorBuffer>> sel_cache_t;

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/value.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/exception.hpp
//
//
//===----------------------------------------------------------------------===//





#include <stdarg.h>
#include <stdexcept>

namespace duckdb {

inline void assert_restrict_function(void *left_start, void *left_end, void *right_start, void *right_end,
                                     const char *fname, int linenr) {
	// assert that the two pointers do not overlap
#ifdef DEBUG
	if (!(left_end <= right_start || right_end <= left_start)) {
		printf("ASSERT RESTRICT FAILED: %s:%d\n", fname, linenr);
		assert(0);
	}
#endif
}

#define ASSERT_RESTRICT(left_start, left_end, right_start, right_end)                                                  \
	assert_restrict_function(left_start, left_end, right_start, right_end, __FILE__, __LINE__)

//===--------------------------------------------------------------------===//
// Exception Types
//===--------------------------------------------------------------------===//

enum class ExceptionType {
	INVALID = 0,          // invalid type
	OUT_OF_RANGE = 1,     // value out of range error
	CONVERSION = 2,       // conversion/casting error
	UNKNOWN_TYPE = 3,     // unknown type
	DECIMAL = 4,          // decimal related
	MISMATCH_TYPE = 5,    // type mismatch
	DIVIDE_BY_ZERO = 6,   // divide by 0
	OBJECT_SIZE = 7,      // object size exceeded
	INVALID_TYPE = 8,     // incompatible for operation
	SERIALIZATION = 9,    // serialization
	TRANSACTION = 10,     // transaction management
	NOT_IMPLEMENTED = 11, // method not implemented
	EXPRESSION = 12,      // expression parsing
	CATALOG = 13,         // catalog related
	PARSER = 14,          // parser related
	PLANNER = 15,         // planner related
	SCHEDULER = 16,       // scheduler related
	EXECUTOR = 17,        // executor related
	CONSTRAINT = 18,      // constraint related
	INDEX = 19,           // index related
	STAT = 20,            // stat related
	CONNECTION = 21,      // connection related
	SYNTAX = 22,          // syntax related
	SETTINGS = 23,        // settings related
	BINDER = 24,          // binder related
	NETWORK = 25,         // network related
	OPTIMIZER = 26,       // optimizer related
	NULL_POINTER = 27,    // nullptr exception
	IO = 28,              // IO exception
	INTERRUPT = 29,       // interrupt
	FATAL = 30, // Fatal exception: fatal exceptions are non-recoverable, and render the entire DB in an unusable state
	INTERNAL =
	    31 // Internal exception: exception that indicates something went wrong internally (i.e. bug in the code base)
};

class Exception : public std::exception {
public:
	Exception(string message);
	Exception(ExceptionType exception_type, string message);

	ExceptionType type;

public:
	const char *what() const noexcept override;

	string ExceptionTypeToString(ExceptionType type);

protected:
	void Format(va_list ap);

private:
	string exception_message_;
};

//===--------------------------------------------------------------------===//
// Exception derived classes
//===--------------------------------------------------------------------===//

//! Exceptions that are StandardExceptions do NOT invalidate the current transaction when thrown
class StandardException : public Exception {
public:
	StandardException(ExceptionType exception_type, string message) : Exception(exception_type, message) {
	}
};

class CatalogException : public StandardException {
public:
	CatalogException(string msg, ...);
};

class ParserException : public StandardException {
public:
	ParserException(string msg, ...);
};

class BinderException : public StandardException {
public:
	BinderException(string msg, ...);
};

class CastException : public Exception {
public:
	CastException(const TypeId origType, const TypeId newType);
};

class ValueOutOfRangeException : public Exception {
public:
	ValueOutOfRangeException(const int64_t value, const TypeId origType, const TypeId newType);
	ValueOutOfRangeException(const double value, const TypeId origType, const TypeId newType);
	ValueOutOfRangeException(const TypeId varType, const idx_t length);
};

class ConversionException : public Exception {
public:
	ConversionException(string msg, ...);
};

class InvalidTypeException : public Exception {
public:
	InvalidTypeException(TypeId type, string msg);
};

class TypeMismatchException : public Exception {
public:
	TypeMismatchException(const TypeId type_1, const TypeId type_2, string msg);
};

class TransactionException : public Exception {
public:
	TransactionException(string msg, ...);
};

class NotImplementedException : public Exception {
public:
	NotImplementedException(string msg, ...);
};

class OutOfRangeException : public Exception {
public:
	OutOfRangeException(string msg, ...);
};

class SyntaxException : public Exception {
public:
	SyntaxException(string msg, ...);
};

class ConstraintException : public Exception {
public:
	ConstraintException(string msg, ...);
};

class IOException : public Exception {
public:
	IOException(string msg, ...);
};

class SerializationException : public Exception {
public:
	SerializationException(string msg, ...);
};

class SequenceException : public Exception {
public:
	SequenceException(string msg, ...);
};

class InterruptException : public Exception {
public:
	InterruptException();
};

class FatalException : public Exception {
public:
	FatalException(string msg, ...);
};

class InternalException : public Exception {
public:
	InternalException(string msg, ...);
};

} // namespace duckdb


#include <iosfwd>
#include <memory.h>

namespace duckdb {

class Deserializer;
class Serializer;

//! The Value object holds a single arbitrary value of any type that can be
//! stored in the database.
class Value {
	friend class Vector;

public:
	//! Create an empty NULL value of the specified type
	Value(TypeId type = TypeId::INT32) : type(type), is_null(true) {
	}
	//! Create a BIGINT value
	Value(int32_t val) : type(TypeId::INT32), is_null(false) {
		value_.integer = val;
	}
	//! Create a FLOAT value
	Value(float val) : type(TypeId::FLOAT), is_null(false) {
		value_.float_ = val;
	}
	//! Create a DOUBLE value
	Value(double val) : type(TypeId::DOUBLE), is_null(false) {
		value_.double_ = val;
	}
	//! Create a VARCHAR value
	Value(const char *val) : Value(val ? string(val) : string()) {
	}
	Value(string_t val);
	//! Create a VARCHAR value
	Value(string val);

	//! Create the lowest possible value of a given type (numeric only)
	static Value MinimumValue(TypeId type);
	//! Create the highest possible value of a given type (numeric only)
	static Value MaximumValue(TypeId type);
	//! Create a Numeric value of the specified type with the specified value
	static Value Numeric(TypeId id, int64_t value);

	//! Create a tinyint Value from a specified value
	static Value BOOLEAN(int8_t value);
	//! Create a tinyint Value from a specified value
	static Value TINYINT(int8_t value);
	//! Create a smallint Value from a specified value
	static Value SMALLINT(int16_t value);
	//! Create an integer Value from a specified value
	static Value INTEGER(int32_t value);
	//! Create a bigint Value from a specified value
	static Value BIGINT(int64_t value);
	//! Create a hash Value from a specified value
	static Value HASH(hash_t value);
	//! Create a pointer Value from a specified value
	static Value POINTER(uintptr_t value);
	//! Create a date Value from a specified date
	static Value DATE(int32_t year, int32_t month, int32_t day);
	//! Create a time Value from a specified date
	static Value TIME(int32_t hour, int32_t min, int32_t sec, int32_t msec);
	//! Create a timestamp Value from a specified date/time combination
	static Value TIMESTAMP(date_t date, dtime_t time);
	//! Create a timestamp Value from a specified timestamp
	static Value TIMESTAMP(timestamp_t timestamp);
	//! Create a timestamp Value from a specified timestamp in separate values
	static Value TIMESTAMP(int32_t year, int32_t month, int32_t day, int32_t hour, int32_t min, int32_t sec,
	                       int32_t msec);

	//! Create a float Value from a specified value
	static Value FLOAT(float value);
	//! Create a double Value from a specified value
	static Value DOUBLE(double value);
	//! Create a struct value with given list of entries
	static Value STRUCT(child_list_t<Value> values);
	//! Create a list value with the given entries
	static Value LIST(std::vector<Value> values);

	template <class T> T GetValue() {
		throw NotImplementedException("Unimplemented template type for Value::GetValue");
	}
	template <class T> static Value CreateValue(T value) {
		throw NotImplementedException("Unimplemented template type for Value::CreateValue");
	}

	//! Return a copy of this value
	Value Copy() const {
		return Value(*this);
	}

	//! Convert this value to a string
	string ToString() const;
	//! Convert this value to a string, with the given display format
	string ToString(SQLType type) const;

	//! Cast this value to another type
	Value CastAs(TypeId target_type) const;
	//! Cast this value to another type
	Value CastAs(SQLType source_type, SQLType target_type);

	//! The type of the value
	TypeId type;
	//! Whether or not the value is NULL
	bool is_null;

	//! The value of the object, if it is of a constant size Type
	union Val {
		int8_t boolean;
		int8_t tinyint;
		int16_t smallint;
		int32_t integer;
		int64_t bigint;
		float float_;
		double double_;
		uintptr_t pointer;
		uint64_t hash;
	} value_;

	//! The value of the object, if it is of a variable size type
	string str_value;

	child_list_t<Value> struct_value;
	std::vector<Value> list_value;

	//! Serializes a Value to a stand-alone binary blob
	void Serialize(Serializer &serializer);
	//! Deserializes a Value from a blob
	static Value Deserialize(Deserializer &source);

	//===--------------------------------------------------------------------===//
	// Numeric Operators
	//===--------------------------------------------------------------------===//
	Value operator+(const Value &rhs) const;
	Value operator-(const Value &rhs) const;
	Value operator*(const Value &rhs) const;
	Value operator/(const Value &rhs) const;
	Value operator%(const Value &rhs) const;

	//===--------------------------------------------------------------------===//
	// Comparison Operators
	//===--------------------------------------------------------------------===//
	bool operator==(const Value &rhs) const;
	bool operator!=(const Value &rhs) const;
	bool operator<(const Value &rhs) const;
	bool operator>(const Value &rhs) const;
	bool operator<=(const Value &rhs) const;
	bool operator>=(const Value &rhs) const;

	bool operator==(const int64_t &rhs) const;
	bool operator!=(const int64_t &rhs) const;
	bool operator<(const int64_t &rhs) const;
	bool operator>(const int64_t &rhs) const;
	bool operator<=(const int64_t &rhs) const;
	bool operator>=(const int64_t &rhs) const;

	static bool IsUTF8String(const char *s);
	static bool IsUTF8String(string_t s);
	//! Returns true if the values are (approximately) equivalent. Note this is NOT the SQL equivalence. For this
	//! function, NULL values are equivalent and floating point values that are close are equivalent.
	static bool ValuesAreEqual(Value result_value, Value value);

	friend std::ostream &operator<<(std::ostream &out, const Value &val) {
		out << val.ToString();
		return out;
	}
	void Print();

private:
	template <class T> T GetValueInternal();
	//! Templated helper function for casting
	template <class DST, class OP> static DST _cast(const Value &v);

	//! Templated helper function for binary operations
	template <class OP>
	static void _templated_binary_operation(const Value &left, const Value &right, Value &result, bool ignore_null);

	//! Templated helper function for boolean operations
	template <class OP> static bool _templated_boolean_operation(const Value &left, const Value &right);
};

template <> Value Value::CreateValue(bool value);
template <> Value Value::CreateValue(int8_t value);
template <> Value Value::CreateValue(int16_t value);
template <> Value Value::CreateValue(int32_t value);
template <> Value Value::CreateValue(int64_t value);
template <> Value Value::CreateValue(const char *value);
template <> Value Value::CreateValue(string value);
template <> Value Value::CreateValue(string_t value);
template <> Value Value::CreateValue(float value);
template <> Value Value::CreateValue(double value);

template <> bool Value::GetValue();
template <> int8_t Value::GetValue();
template <> int16_t Value::GetValue();
template <> int32_t Value::GetValue();
template <> int64_t Value::GetValue();
template <> string Value::GetValue();
template <> float Value::GetValue();
template <> double Value::GetValue();

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/vector_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

enum class VectorType : uint8_t {
	FLAT_VECTOR,       // Flat vectors represent a standard uncompressed vector
	CONSTANT_VECTOR,   // Constant vector represents a single constant
	DICTIONARY_VECTOR, // Dictionary vector represents a selection vector on top of another vector
	SEQUENCE_VECTOR    // Sequence vector represents a sequence with a start point and an increment
};

string VectorTypeToString(VectorType type);

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/vector_buffer.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/string_heap.hpp
//
//
//===----------------------------------------------------------------------===//






namespace duckdb {
//! A string heap is the owner of a set of strings, strings can be inserted into
//! it On every insert, a pointer to the inserted string is returned The
//! returned pointer will remain valid until the StringHeap is destroyed
class StringHeap {
public:
	StringHeap();

	void Destroy() {
		tail = nullptr;
		chunk = nullptr;
	}

	void Move(StringHeap &other) {
		assert(!other.chunk);
		other.tail = tail;
		other.chunk = move(chunk);
		tail = nullptr;
	}

	//! Add a string to the string heap, returns a pointer to the string
	string_t AddString(const char *data, idx_t len);
	//! Add a string to the string heap, returns a pointer to the string
	string_t AddString(const char *data);
	//! Add a string to the string heap, returns a pointer to the string
	string_t AddString(const string &data);
	//! Add a string to the string heap, returns a pointer to the string
	string_t AddString(const string_t &data);
	//! Allocates space for an empty string of size "len" on the heap
	string_t EmptyString(idx_t len);
	//! Add all strings from a different string heap to this string heap
	void MergeHeap(StringHeap &heap);

private:
	struct StringChunk {
		StringChunk(idx_t size) : current_position(0), maximum_size(size) {
			data = unique_ptr<char[]>(new char[maximum_size]);
		}
		~StringChunk() {
			if (prev) {
				auto current_prev = move(prev);
				while (current_prev) {
					current_prev = move(current_prev->prev);
				}
			}
		}

		unique_ptr<char[]> data;
		idx_t current_position;
		idx_t maximum_size;
		unique_ptr<StringChunk> prev;
	};
	StringChunk *tail;
	unique_ptr<StringChunk> chunk;
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/string_type.hpp
//
//
//===----------------------------------------------------------------------===//




#include <cstring>
#include <cassert>

namespace duckdb {

struct string_t {
	friend struct StringComparisonOperators;
	friend class StringSegment;

public:
	static constexpr idx_t PREFIX_LENGTH = 4 * sizeof(char);
	static constexpr idx_t INLINE_LENGTH = 12;

	string_t() = default;
	string_t(uint32_t len) : length(len) {
		memset(prefix, 0, PREFIX_LENGTH);
		value_.data = nullptr;
	}
	string_t(const char *data, uint32_t len) : length(len) {
		assert(data || length == 0);
		if (IsInlined()) {
			// zero initialize the prefix first
			// this makes sure that strings with length smaller than 4 still have an equal prefix
			memset(prefix, 0, PREFIX_LENGTH);
			if (length == 0) {
				return;
			}
			// small string: inlined
			memcpy(prefix, data, length);
			prefix[length] = '\0';
		} else {
			// large string: store pointer
			memcpy(prefix, data, PREFIX_LENGTH);
			value_.data = (char *)data;
		}
	}
	string_t(const char *data) : string_t(data, strlen(data)) {
	}
	string_t(const string &value) : string_t(value.c_str(), value.size()) {
	}

	bool IsInlined() const {
		return length < INLINE_LENGTH;
	}

	char *GetData() {
		return IsInlined() ? (char *)prefix : value_.data;
	}

	const char *GetData() const {
		return IsInlined() ? (const char *)prefix : value_.data;
	}

	const char *GetPrefix() const {
		return prefix;
	}

	idx_t GetSize() const {
		return length;
	}

	string GetString() const {
		return string(GetData(), GetSize());
	}

	void Finalize() {
		// set trailing NULL byte
		auto dataptr = (char *)GetData();
		dataptr[length] = '\0';
		if (length < INLINE_LENGTH) {
			// fill prefix with zeros if the length is smaller than the prefix length
			for (idx_t i = length; i < PREFIX_LENGTH; i++) {
				prefix[i] = '\0';
			}
		} else {
			// copy the data into the prefix
			memcpy(prefix, dataptr, PREFIX_LENGTH);
		}
	}

	void Verify();

private:
	uint32_t length;
	char prefix[4];
	union {
		char inlined[8];
		char *data;
	} value_;
};

}; // namespace duckdb



namespace duckdb {

class VectorBuffer;
class Vector;
class ChunkCollection;

enum class VectorBufferType : uint8_t {
	STANDARD_BUFFER,     // standard buffer, holds a single array of data
	DICTIONARY_BUFFER,   // dictionary buffer, holds a selection vector
	VECTOR_CHILD_BUFFER, // vector child buffer: holds another vector
	STRING_BUFFER,       // string buffer, holds a string heap
	STRUCT_BUFFER,       // struct buffer, holds a ordered mapping from name to child vector
	LIST_BUFFER          // list buffer, holds a single flatvector child
};

//! The VectorBuffer is a class used by the vector to hold its data
class VectorBuffer {
public:
	VectorBuffer(VectorBufferType type) : type(type) {
	}
	VectorBuffer(idx_t data_size);
	virtual ~VectorBuffer() {
	}

	VectorBufferType type;

public:
	data_ptr_t GetData() {
		return data.get();
	}

	static buffer_ptr<VectorBuffer> CreateStandardVector(TypeId type);
	static buffer_ptr<VectorBuffer> CreateConstantVector(TypeId type);

protected:
	unique_ptr<data_t[]> data;
};

//! The DictionaryBuffer holds a selection vector
class DictionaryBuffer : public VectorBuffer {
public:
	DictionaryBuffer(const SelectionVector &sel) : VectorBuffer(VectorBufferType::DICTIONARY_BUFFER), sel_vector(sel) {
	}
	DictionaryBuffer(buffer_ptr<SelectionData> data)
	    : VectorBuffer(VectorBufferType::DICTIONARY_BUFFER), sel_vector(move(data)) {
	}
	DictionaryBuffer(idx_t count = STANDARD_VECTOR_SIZE)
	    : VectorBuffer(VectorBufferType::DICTIONARY_BUFFER), sel_vector(count) {
	}

public:
	SelectionVector &GetSelVector() {
		return sel_vector;
	}

private:
	SelectionVector sel_vector;
};

class VectorStringBuffer : public VectorBuffer {
public:
	VectorStringBuffer();

public:
	string_t AddString(const char *data, idx_t len) {
		return heap.AddString(data, len);
	}
	string_t AddString(string_t data) {
		return heap.AddString(data);
	}
	string_t EmptyString(idx_t len) {
		return heap.EmptyString(len);
	}

	void AddHeapReference(buffer_ptr<VectorBuffer> heap) {
		references.push_back(move(heap));
	}

private:
	//! The string heap of this buffer
	StringHeap heap;
	// References to additional vector buffers referenced by this string buffer
	vector<buffer_ptr<VectorBuffer>> references;
};

class VectorStructBuffer : public VectorBuffer {
public:
	VectorStructBuffer();
	~VectorStructBuffer();

public:
	child_list_t<unique_ptr<Vector>> &GetChildren() {
		return children;
	}
	void AddChild(string name, unique_ptr<Vector> vector) {
		children.push_back(std::make_pair(name, move(vector)));
	}

private:
	//! child vectors used for nested data
	child_list_t<unique_ptr<Vector>> children;
};

class VectorListBuffer : public VectorBuffer {
public:
	VectorListBuffer();

	~VectorListBuffer();

public:
	ChunkCollection &GetChild() {
		return *child;
	}
	void SetChild(unique_ptr<ChunkCollection> new_child);

private:
	//! child vectors used for nested data
	unique_ptr<ChunkCollection> child;
};

} // namespace duckdb


namespace duckdb {
//! Type used for nullmasks
typedef bitset<STANDARD_VECTOR_SIZE> nullmask_t;

//! Zero NULL mask: filled with the value 0 [READ ONLY]
extern nullmask_t ZERO_MASK;

struct VectorData {
	const SelectionVector *sel;
	data_ptr_t data;
	nullmask_t *nullmask;
};

class VectorStructBuffer;
class VectorListBuffer;
class ChunkCollection;

//!  Vector of values of a specified TypeId.
class Vector {
	friend struct ConstantVector;
	friend struct DictionaryVector;
	friend struct FlatVector;
	friend struct ListVector;
	friend struct StringVector;
	friend struct StructVector;
	friend struct SequenceVector;

	friend class DataChunk;

public:
	Vector();
	//! Create a vector of size one holding the passed on value
	Vector(Value value);
	//! Create an empty standard vector with a type, equivalent to calling Vector(type, true, false)
	Vector(TypeId type);
	//! Create a non-owning vector that references the specified data
	Vector(TypeId type, data_ptr_t dataptr);
	//! Create an owning vector that holds at most STANDARD_VECTOR_SIZE entries.
	/*!
	    Create a new vector
	    If create_data is true, the vector will be an owning empty vector.
	    If zero_data is true, the allocated data will be zero-initialized.
	*/
	Vector(TypeId type, bool create_data, bool zero_data);
	// implicit copying of Vectors is not allowed
	Vector(const Vector &) = delete;
	// but moving of vectors is allowed
	Vector(Vector &&other) noexcept;

	//! The vector type specifies how the data of the vector is physically stored (i.e. if it is a single repeated
	//! constant, if it is compressed)
	VectorType vector_type;
	//! The type of the elements stored in the vector (e.g. integer, float)
	TypeId type;

public:
	//! Create a vector that references the specified value.
	void Reference(Value &value);
	//! Causes this vector to reference the data held by the other vector.
	void Reference(Vector &other);

	//! Creates a reference to a slice of the other vector
	void Slice(Vector &other, idx_t offset);
	//! Creates a reference to a slice of the other vector
	void Slice(Vector &other, const SelectionVector &sel, idx_t count);
	//! Turns the vector into a dictionary vector with the specified dictionary
	void Slice(const SelectionVector &sel, idx_t count);
	//! Slice the vector, keeping the result around in a cache or potentially using the cache instead of slicing
	void Slice(const SelectionVector &sel, idx_t count, sel_cache_t &cache);

	//! Creates the data of this vector with the specified type. Any data that
	//! is currently in the vector is destroyed.
	void Initialize(TypeId new_type = TypeId::INVALID, bool zero_data = false);

	//! Converts this Vector to a printable string representation
	string ToString(idx_t count) const;
	void Print(idx_t count);

	string ToString() const;
	void Print();

	//! Flatten the vector, removing any compression and turning it into a FLAT_VECTOR
	void Normalify(idx_t count);
	void Normalify(const SelectionVector &sel, idx_t count);
	//! Obtains a selection vector and data pointer through which the data of this vector can be accessed
	void Orrify(idx_t count, VectorData &data);

	//! Turn the vector into a sequence vector
	void Sequence(int64_t start, int64_t increment);

	//! Verify that the Vector is in a consistent, not corrupt state. DEBUG
	//! FUNCTION ONLY!
	void Verify(idx_t count);
	void Verify(const SelectionVector &sel, idx_t count);

	//! Returns the [index] element of the Vector as a Value.
	Value GetValue(idx_t index) const;
	//! Sets the [index] element of the Vector to the specified Value.
	void SetValue(idx_t index, Value val);

	//! Serializes a Vector to a stand-alone binary blob
	void Serialize(idx_t count, Serializer &serializer);
	//! Deserializes a blob back into a Vector
	void Deserialize(idx_t count, Deserializer &source);

protected:
	//! A pointer to the data.
	data_ptr_t data;
	//! The nullmask of the vector
	nullmask_t nullmask;
	//! The main buffer holding the data of the vector
	buffer_ptr<VectorBuffer> buffer;
	//! The buffer holding auxiliary data of the vector
	//! e.g. a string vector uses this to store strings
	buffer_ptr<VectorBuffer> auxiliary;
};

//! The DictionaryBuffer holds a selection vector
class VectorChildBuffer : public VectorBuffer {
public:
	VectorChildBuffer() : VectorBuffer(VectorBufferType::VECTOR_CHILD_BUFFER), data() {
	}

public:
	Vector data;
};

struct ConstantVector {
	static inline data_ptr_t GetData(Vector &vector) {
		assert(vector.vector_type == VectorType::CONSTANT_VECTOR || vector.vector_type == VectorType::FLAT_VECTOR);
		return vector.data;
	}
	template <class T> static inline T *GetData(Vector &vector) {
		return (T *)ConstantVector::GetData(vector);
	}
	static inline bool IsNull(const Vector &vector) {
		assert(vector.vector_type == VectorType::CONSTANT_VECTOR);
		return vector.nullmask[0];
	}
	static inline void SetNull(Vector &vector, bool is_null) {
		assert(vector.vector_type == VectorType::CONSTANT_VECTOR);
		vector.nullmask[0] = is_null;
	}
	static inline nullmask_t &Nullmask(Vector &vector) {
		assert(vector.vector_type == VectorType::CONSTANT_VECTOR);
		return vector.nullmask;
	}

	static const sel_t zero_vector[STANDARD_VECTOR_SIZE];
	static const SelectionVector ZeroSelectionVector;
};

struct DictionaryVector {
	static inline SelectionVector &SelVector(const Vector &vector) {
		assert(vector.vector_type == VectorType::DICTIONARY_VECTOR);
		return ((DictionaryBuffer &)*vector.buffer).GetSelVector();
	}
	static inline Vector &Child(const Vector &vector) {
		assert(vector.vector_type == VectorType::DICTIONARY_VECTOR);
		return ((VectorChildBuffer &)*vector.auxiliary).data;
	}
};

struct FlatVector {
	static inline data_ptr_t GetData(Vector &vector) {
		return ConstantVector::GetData(vector);
	}
	template <class T> static inline T *GetData(Vector &vector) {
		return ConstantVector::GetData<T>(vector);
	}
	template <class T> static inline T GetValue(Vector &vector, idx_t idx) {
		assert(vector.vector_type == VectorType::FLAT_VECTOR);
		return FlatVector::GetData<T>(vector)[idx];
	}
	static inline nullmask_t &Nullmask(Vector &vector) {
		assert(vector.vector_type == VectorType::FLAT_VECTOR);
		return vector.nullmask;
	}
	static inline void SetNullmask(Vector &vector, nullmask_t new_mask) {
		assert(vector.vector_type == VectorType::FLAT_VECTOR);
		vector.nullmask = move(new_mask);
	}
	static inline void SetNull(Vector &vector, idx_t idx, bool value) {
		assert(vector.vector_type == VectorType::FLAT_VECTOR);
		vector.nullmask[idx] = value;
	}
	static inline bool IsNull(const Vector &vector, idx_t idx) {
		assert(vector.vector_type == VectorType::FLAT_VECTOR);
		return vector.nullmask[idx];
	}

	static const sel_t incremental_vector[STANDARD_VECTOR_SIZE];
	static const SelectionVector IncrementalSelectionVector;
};

struct ListVector {
	static ChunkCollection &GetEntry(const Vector &vector);
	static bool HasEntry(const Vector &vector);
	static void SetEntry(Vector &vector, unique_ptr<ChunkCollection> entry);
};

struct StringVector {
	//! Add a string to the string heap of the vector (auxiliary data)
	static string_t AddString(Vector &vector, const char *data, idx_t len);
	//! Add a string to the string heap of the vector (auxiliary data)
	static string_t AddString(Vector &vector, const char *data);
	//! Add a string to the string heap of the vector (auxiliary data)
	static string_t AddString(Vector &vector, string_t data);
	//! Add a string to the string heap of the vector (auxiliary data)
	static string_t AddString(Vector &vector, const string &data);
	//! Allocates an empty string of the specified size, and returns a writable pointer that can be used to store the
	//! result of an operation
	static string_t EmptyString(Vector &vector, idx_t len);

	//! Add a reference from this vector to the string heap of the provided vector
	static void AddHeapReference(Vector &vector, Vector &other);
};

struct StructVector {
	static bool HasEntries(const Vector &vector);
	static child_list_t<unique_ptr<Vector>> &GetEntries(const Vector &vector);
	static void AddEntry(Vector &vector, string name, unique_ptr<Vector> entry);
};

struct SequenceVector {
	static void GetSequence(const Vector &vector, int64_t &start, int64_t &increment) {
		assert(vector.vector_type == VectorType::SEQUENCE_VECTOR);
		auto data = (int64_t *)vector.buffer->GetData();
		start = data[0];
		increment = data[1];
	}
};

class StandaloneVector : public Vector {
public:
	StandaloneVector() : Vector() {
	}
	StandaloneVector(TypeId type) : Vector(type) {
	}
	StandaloneVector(TypeId type, data_ptr_t dataptr) : Vector(type, dataptr) {
	}

public:
	idx_t size() {
		return count;
	}
	void SetCount(idx_t count) {
		assert(count <= STANDARD_VECTOR_SIZE);
		this->count = count;
	}

protected:
	idx_t count;
};

} // namespace duckdb


#include <vector>

namespace duckdb {

//!  A Data Chunk represents a set of vectors.
/*!
    The data chunk class is the intermediate representation used by the
   execution engine of DuckDB. It effectively represents a subset of a relation.
   It holds a set of vectors that all have the same length.

    DataChunk is initialized using the DataChunk::Initialize function by
   providing it with a vector of TypeIds for the Vector members. By default,
   this function will also allocate a chunk of memory in the DataChunk for the
   vectors and all the vectors will be referencing vectors to the data owned by
   the chunk. The reason for this behavior is that the underlying vectors can
   become referencing vectors to other chunks as well (i.e. in the case an
   operator does not alter the data, such as a Filter operator which only adds a
   selection vector).

    In addition to holding the data of the vectors, the DataChunk also owns the
   selection vector that underlying vectors can point to.
*/
class DataChunk {
public:
	//! Creates an empty DataChunk
	DataChunk();

	//! The vectors owned by the DataChunk.
	vector<Vector> data;

public:
	idx_t size() const {
		return count;
	}
	idx_t column_count() const {
		return data.size();
	}
	void SetCardinality(idx_t count) {
		assert(count <= STANDARD_VECTOR_SIZE);
		this->count = count;
	}
	void SetCardinality(const DataChunk &other) {
		this->count = other.size();
	}

	Value GetValue(idx_t col_idx, idx_t index) const;
	void SetValue(idx_t col_idx, idx_t index, Value val);

	//! Set the DataChunk to reference another data chunk
	void Reference(DataChunk &chunk);

	//! Initializes the DataChunk with the specified types to an empty DataChunk
	//! This will create one vector of the specified type for each TypeId in the
	//! types list. The vector will be referencing vector to the data owned by
	//! the DataChunk.
	void Initialize(vector<TypeId> &types);
	//! Initializes an empty DataChunk with the given types. The vectors will *not* have any data allocated for them.
	void InitializeEmpty(vector<TypeId> &types);
	//! Append the other DataChunk to this one. The column count and types of
	//! the two DataChunks have to match exactly. Throws an exception if there
	//! is not enough space in the chunk.
	void Append(DataChunk &other);
	//! Destroy all data and columns owned by this DataChunk
	void Destroy();

	//! Copies the data from this vector to another vector.
	void Copy(DataChunk &other, idx_t offset = 0);

	//! Turn all the vectors from the chunk into flat vectors
	void Normalify();

	unique_ptr<VectorData[]> Orrify();

	void Slice(const SelectionVector &sel_vector, idx_t count);
	void Slice(DataChunk &other, const SelectionVector &sel, idx_t count, idx_t col_offset = 0);

	//! Resets the DataChunk to its state right after the DataChunk::Initialize
	//! function was called. This sets the count to 0, and resets each member
	//! Vector to point back to the data owned by this DataChunk.
	void Reset();

	//! Serializes a DataChunk to a stand-alone binary blob
	void Serialize(Serializer &serializer);
	//! Deserializes a blob back into a DataChunk
	void Deserialize(Deserializer &source);

	//! Hashes the DataChunk to the target vector
	void Hash(Vector &result);

	//! Returns a list of types of the vectors of this data chunk
	vector<TypeId> GetTypes();

	//! Converts this DataChunk to a printable string representation
	string ToString() const;
	void Print();

	DataChunk(const DataChunk &) = delete;

	//! Verify that the DataChunk is in a consistent, not corrupt state. DEBUG
	//! FUNCTION ONLY!
	void Verify();

private:
	idx_t count;
};
} // namespace duckdb


namespace duckdb {

//!  A ChunkCollection represents a set of DataChunks that all have the same
//!  types
/*!
    A ChunkCollection represents a set of DataChunks concatenated together in a
   list. Individual values of the collection can be iterated over using the
   iterator. It is also possible to iterate directly over the chunks for more
   direct access.
*/
class ChunkCollection {
public:
	ChunkCollection() : count(0) {
	}

	//! The total amount of elements in the collection
	idx_t count;
	//! The set of data chunks in the collection
	vector<unique_ptr<DataChunk>> chunks;
	//! The types of the ChunkCollection
	vector<TypeId> types;

	//! The amount of columns in the ChunkCollection
	idx_t column_count() {
		return types.size();
	}

	//! Append a new DataChunk directly to this ChunkCollection
	void Append(DataChunk &new_chunk);

	//! Append another ChunkCollection directly to this ChunkCollection
	void Append(ChunkCollection &other);

	void Verify();

	//! Gets the value of the column at the specified index
	Value GetValue(idx_t column, idx_t index);
	//! Sets the value of the column at the specified index
	void SetValue(idx_t column, idx_t index, Value value);

	vector<Value> GetRow(idx_t index);

	string ToString() const {
		return chunks.size() == 0 ? "ChunkCollection [ 0 ]"
		                          : "ChunkCollection [ " + std::to_string(count) + " ]: \n" + chunks[0]->ToString();
	}
	void Print();

	//! Gets a reference to the chunk at the given index
	DataChunk &GetChunk(idx_t index) {
		return *chunks[LocateChunk(index)];
	}

	void Sort(vector<OrderType> &desc, idx_t result[]);
	//! Reorders the rows in the collection according to the given indices. NB: order is changed!
	void Reorder(idx_t order[]);

	void MaterializeSortedChunk(DataChunk &target, idx_t order[], idx_t start_offset);

	//! Returns true if the ChunkCollections are equivalent
	bool Equals(ChunkCollection &other);

	//! Locates the chunk that belongs to the specific index
	idx_t LocateChunk(idx_t index) {
		idx_t result = index / STANDARD_VECTOR_SIZE;
		assert(result < chunks.size());
		return result;
	}

	void Heap(vector<OrderType> &desc, idx_t heap[], idx_t heap_size);
	idx_t MaterializeHeapChunk(DataChunk &target, idx_t order[], idx_t start_offset, idx_t heap_size);
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/query_result.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/statement_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Statement Types
//===--------------------------------------------------------------------===//
enum class StatementType : uint8_t {
	INVALID,      // invalid statement type
	SELECT,       // select statement type
	INSERT,       // insert statement type
	UPDATE,       // update statement type
	CREATE,       // create statement type
	DELETE,       // delete statement type
	PREPARE,      // prepare statement type
	EXECUTE,      // execute statement type
	ALTER,        // alter statement type
	TRANSACTION,  // transaction statement type,
	COPY,         // copy type
	ANALYZE,      // analyze type
	VARIABLE_SET, // variable set statement type
	CREATE_FUNC,  // create func statement type
	EXPLAIN,      // explain statement type
	DROP,         // DROP statement type
	PRAGMA,       // PRAGMA statement type
	VACUUM,       // VACUUM statement type
};

string StatementTypeToString(StatementType type);

} // namespace duckdb


namespace duckdb {

enum class QueryResultType : uint8_t { MATERIALIZED_RESULT, STREAM_RESULT };

//! The QueryResult object holds the result of a query. It can either be a MaterializedQueryResult, in which case the
//! result contains the entire result set, or a StreamQueryResult in which case the Fetch method can be called to
//! incrementally fetch data from the database.
class QueryResult {
public:
	//! Creates an successful empty query result
	QueryResult(QueryResultType type, StatementType statement_type);
	//! Creates a successful query result with the specified names and types
	QueryResult(QueryResultType type, StatementType statement_type, vector<SQLType> sql_types, vector<TypeId> types,
	            vector<string> names);
	//! Creates an unsuccessful query result with error condition
	QueryResult(QueryResultType type, string error);
	virtual ~QueryResult() {
	}

	//! The type of the result (MATERIALIZED or STREAMING)
	QueryResultType type;
	//! The type of the statement that created this result
	StatementType statement_type;
	//! The SQL types of the result
	vector<SQLType> sql_types;
	//! The types of the result
	vector<TypeId> types;
	//! The names of the result
	vector<string> names;
	//! Whether or not execution was successful
	bool success;
	//! The error string (in case execution was not successful)
	string error;
	//! The next result (if any)
	unique_ptr<QueryResult> next;

public:
	//! Fetches a DataChunk from the query result. Returns an empty chunk if the result is empty, or nullptr on failure.
	virtual unique_ptr<DataChunk> Fetch() = 0;
	// Converts the QueryResult to a string
	virtual string ToString() = 0;
	//! Prints the QueryResult to the console
	void Print();
	//! Returns true if the two results are identical; false otherwise. Note that this method is destructive; it calls
	//! Fetch() until both results are exhausted. The data in the results will be lost.
	bool Equals(QueryResult &other);

private:
	//! The current chunk used by the iterator
	unique_ptr<DataChunk> iterator_chunk;

	class QueryResultIterator;

	class QueryResultRow {
	public:
		QueryResultRow(QueryResultIterator &iterator) : iterator(iterator), row(0) {
		}

		QueryResultIterator &iterator;
		idx_t row;

		template <class T> T GetValue(idx_t col_idx) const {
			return iterator.result->iterator_chunk->GetValue(col_idx, iterator.row_idx).GetValue<T>();
		}
	};
	//! The row-based query result iterator. Invoking the
	class QueryResultIterator {
	public:
		QueryResultIterator(QueryResult *result) : current_row(*this), result(result), row_idx(0) {
			if (result) {
				result->iterator_chunk = result->Fetch();
			}
		}

		QueryResultRow current_row;
		QueryResult *result;
		idx_t row_idx;

	public:
		void Next() {
			if (!result->iterator_chunk) {
				return;
			}
			current_row.row++;
			row_idx++;
			if (row_idx >= result->iterator_chunk->size()) {
				result->iterator_chunk = result->Fetch();
				row_idx = 0;
			}
		}

		QueryResultIterator &operator++() {
			Next();
			return *this;
		}
		bool operator!=(const QueryResultIterator &other) const {
			return result->iterator_chunk && result->iterator_chunk->column_count() > 0;
		}
		const QueryResultRow &operator*() const {
			return current_row;
		}
	};

public:
	QueryResultIterator begin() {
		return QueryResultIterator(this);
	}
	QueryResultIterator end() {
		return QueryResultIterator(nullptr);
	}

protected:
	string HeaderToString();

private:
	QueryResult(const QueryResult &) = delete;
};

} // namespace duckdb


namespace duckdb {

class MaterializedQueryResult : public QueryResult {
public:
	//! Creates an empty successful query result
	MaterializedQueryResult(StatementType statement_type);
	//! Creates a successful query result with the specified names and types
	MaterializedQueryResult(StatementType statement_type, vector<SQLType> sql_types, vector<TypeId> types,
	                        vector<string> names);
	//! Creates an unsuccessful query result with error condition
	MaterializedQueryResult(string error);

	//! Fetches a DataChunk from the query result. Returns an empty chunk if the result is empty, or nullptr on failure.
	//! This will consume the result (i.e. the chunks are taken directly from the ChunkCollection).
	unique_ptr<DataChunk> Fetch() override;
	//! Converts the QueryResult to a string
	string ToString() override;

	//! Gets the (index) value of the (column index) column
	Value GetValue(idx_t column, idx_t index);

	template <class T> T GetValue(idx_t column, idx_t index) {
		auto value = GetValue(column, index);
		return (T)value.GetValue<int64_t>();
	}

	ChunkCollection collection;
};

} // namespace duckdb


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/stream_query_result.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

class ClientContext;
class MaterializedQueryResult;

class StreamQueryResult : public QueryResult {
public:
	//! Create a successful StreamQueryResult. StreamQueryResults should always be successful initially (it makes no
	//! sense to stream an error).
	StreamQueryResult(StatementType statement_type, ClientContext &context, vector<SQLType> sql_types,
	                  vector<TypeId> types, vector<string> names);
	~StreamQueryResult() override;

	//! Fetches a DataChunk from the query result. Returns an empty chunk if the result is empty, or nullptr on error.
	unique_ptr<DataChunk> Fetch() override;
	//! Converts the QueryResult to a string
	string ToString() override;
	//! Materializes the query result and turns it into a materialized query result
	unique_ptr<MaterializedQueryResult> Materialize();

	//! Closes the StreamQueryResult
	void Close();

	//! Whether or not the StreamQueryResult is still open
	bool is_open;

private:
	//! The client context this StreamQueryResult belongs to
	ClientContext &context;
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/prepared_statement.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {
class ClientContext;
class PreparedStatementData;

//! A prepared statement
class PreparedStatement {
public:
	//! Create a successfully prepared prepared statement object with the given name
	PreparedStatement(ClientContext *context, string name, string query, PreparedStatementData &data,
	                  idx_t n_param = 0);
	//! Create a prepared statement that was not successfully prepared
	PreparedStatement(string error);

	~PreparedStatement();

public:
	StatementType type;
	//! The client context this prepared statement belongs to
	ClientContext *context;
	//! The internal name of the prepared statement
	string name;
	//! The query that is being prepared
	string query;
	//! Whether or not the statement was successfully prepared
	bool success;
	//! The error message (if success = false)
	string error;
	//! Whether or not the prepared statement has been invalidated because the underlying connection has been destroyed
	bool is_invalidated;
	//! The amount of bound parameters
	idx_t n_param;
	//! The result SQL types of the prepared statement
	vector<SQLType> types;
	//! The result names of the prepared statement
	vector<string> names;

public:
	//! Execute the prepared statement with the given set of arguments
	template <typename... Args> unique_ptr<QueryResult> Execute(Args... args) {
		vector<Value> values;
		return ExecuteRecursive(values, args...);
	}

	//! Execute the prepared statement with the given set of values
	unique_ptr<QueryResult> Execute(vector<Value> &values, bool allow_stream_result = true);

private:
	unique_ptr<QueryResult> ExecuteRecursive(vector<Value> &values) {
		return Execute(values);
	}

	template <typename T, typename... Args>
	unique_ptr<QueryResult> ExecuteRecursive(vector<Value> &values, T value, Args... args) {
		values.push_back(Value::CreateValue<T>(value));
		return ExecuteRecursive(values, args...);
	}
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/table_description.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/column_definition.hpp
//
//
//===----------------------------------------------------------------------===//





//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_expression.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/base_expression.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/expression_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Predicate Expression Operation Types
//===--------------------------------------------------------------------===//
enum class ExpressionType : uint8_t {
	INVALID = 0,

	// explicitly cast left as right (right is integer in ValueType enum)
	OPERATOR_CAST = 12,
	// logical not operator
	OPERATOR_NOT = 13,
	// is null operator
	OPERATOR_IS_NULL = 14,
	// is not null operator
	OPERATOR_IS_NOT_NULL = 15,

	// -----------------------------
	// Comparison Operators
	// -----------------------------
	// equal operator between left and right
	COMPARE_EQUAL = 25,
	// compare initial boundary
	COMPARE_BOUNDARY_START = COMPARE_EQUAL,
	// inequal operator between left and right
	COMPARE_NOTEQUAL = 26,
	// less than operator between left and right
	COMPARE_LESSTHAN = 27,
	// greater than operator between left and right
	COMPARE_GREATERTHAN = 28,
	// less than equal operator between left and right
	COMPARE_LESSTHANOREQUALTO = 29,
	// greater than equal operator between left and right
	COMPARE_GREATERTHANOREQUALTO = 30,
	// IN operator [left IN (right1, right2, ...)]
	COMPARE_IN = 35,
	// NOT IN operator [left NOT IN (right1, right2, ...)]
	COMPARE_NOT_IN = 36,
	// IS DISTINCT FROM operator
	COMPARE_DISTINCT_FROM = 37,
	// compare final boundary

	COMPARE_BETWEEN = 38,
	COMPARE_NOT_BETWEEN = 39,
	COMPARE_BOUNDARY_END = COMPARE_NOT_BETWEEN,

	// -----------------------------
	// Conjunction Operators
	// -----------------------------
	CONJUNCTION_AND = 50,
	CONJUNCTION_OR = 51,

	// -----------------------------
	// Values
	// -----------------------------
	VALUE_CONSTANT = 75,
	VALUE_PARAMETER = 76,
	VALUE_TUPLE = 77,
	VALUE_TUPLE_ADDRESS = 78,
	VALUE_NULL = 79,
	VALUE_VECTOR = 80,
	VALUE_SCALAR = 81,
	VALUE_DEFAULT = 82,

	// -----------------------------
	// Aggregates
	// -----------------------------
	AGGREGATE = 100,
	BOUND_AGGREGATE = 101,

	// -----------------------------
	// Window Functions
	// -----------------------------
	WINDOW_AGGREGATE = 110,

	WINDOW_RANK = 120,
	WINDOW_RANK_DENSE = 121,
	WINDOW_NTILE = 122,
	WINDOW_PERCENT_RANK = 123,
	WINDOW_CUME_DIST = 124,
	WINDOW_ROW_NUMBER = 125,

	WINDOW_FIRST_VALUE = 130,
	WINDOW_LAST_VALUE = 131,
	WINDOW_LEAD = 132,
	WINDOW_LAG = 133,

	// -----------------------------
	// Functions
	// -----------------------------
	FUNCTION = 140,
	BOUND_FUNCTION = 141,

	// -----------------------------
	// Operators
	// -----------------------------
	CASE_EXPR = 150,
	OPERATOR_NULLIF = 151,
	OPERATOR_COALESCE = 152,

	// -----------------------------
	// Subquery IN/EXISTS
	// -----------------------------
	SUBQUERY = 175,

	// -----------------------------
	// Parser
	// -----------------------------
	STAR = 200,
	TABLE_STAR = 201,
	PLACEHOLDER = 202,
	COLUMN_REF = 203,
	FUNCTION_REF = 204,
	TABLE_REF = 205,

	// -----------------------------
	// Miscellaneous
	// -----------------------------
	CAST = 225,
	COMMON_SUBEXPRESSION = 226,
	BOUND_REF = 227,
	BOUND_COLUMN_REF = 228,
	BOUND_UNNEST = 229
};

//===--------------------------------------------------------------------===//
// Expression Class
//===--------------------------------------------------------------------===//
enum class ExpressionClass : uint8_t {
	INVALID = 0,
	//===--------------------------------------------------------------------===//
	// Parsed Expressions
	//===--------------------------------------------------------------------===//
	AGGREGATE = 1,
	CASE = 2,
	CAST = 3,
	COLUMN_REF = 4,
	COMPARISON = 5,
	CONJUNCTION = 6,
	CONSTANT = 7,
	DEFAULT = 8,
	FUNCTION = 9,
	OPERATOR = 10,
	STAR = 11,
	TABLE_STAR = 12,
	SUBQUERY = 13,
	WINDOW = 14,
	PARAMETER = 15,
	//===--------------------------------------------------------------------===//
	// Bound Expressions
	//===--------------------------------------------------------------------===//
	BOUND_AGGREGATE = 25,
	BOUND_CASE = 26,
	BOUND_CAST = 27,
	BOUND_COLUMN_REF = 28,
	BOUND_COMPARISON = 29,
	BOUND_CONJUNCTION = 30,
	BOUND_CONSTANT = 31,
	BOUND_DEFAULT = 32,
	BOUND_FUNCTION = 33,
	BOUND_OPERATOR = 34,
	BOUND_PARAMETER = 35,
	BOUND_REF = 36,
	BOUND_SUBQUERY = 37,
	BOUND_WINDOW = 38,
	BOUND_BETWEEN = 39,
	BOUND_UNNEST = 40,
	//===--------------------------------------------------------------------===//
	// Miscellaneous
	//===--------------------------------------------------------------------===//
	BOUND_EXPRESSION = 50,
	COMMON_SUBEXPRESSION = 51
};

string ExpressionTypeToString(ExpressionType type);
string ExpressionTypeToOperator(ExpressionType type);

//! Negate a comparison expression, turning e.g. = into !=, or < into >=
ExpressionType NegateComparisionExpression(ExpressionType type);
//! Flip a comparison expression, turning e.g. < into >, or = into =
ExpressionType FlipComparisionExpression(ExpressionType type);

} // namespace duckdb


namespace duckdb {

//!  The BaseExpression class is a base class that can represent any expression
//!  part of a SQL statement.
class BaseExpression {
public:
	//! Create an Expression
	BaseExpression(ExpressionType type, ExpressionClass expression_class)
	    : type(type), expression_class(expression_class) {
	}
	virtual ~BaseExpression() {
	}

	//! Returns the type of the expression
	ExpressionType GetExpressionType() {
		return type;
	}
	//! Returns the class of the expression
	ExpressionClass GetExpressionClass() {
		return expression_class;
	}

	//! Type of the expression
	ExpressionType type;
	//! The expression class of the node
	ExpressionClass expression_class;
	//! The alias of the expression,
	string alias;

public:
	//! Returns true if this expression is an aggregate or not.
	/*!
	 Examples:

	 (1) SUM(a) + 1 -- True

	 (2) a + 1 -- False
	 */
	virtual bool IsAggregate() const = 0;
	//! Returns true if the expression has a window function or not
	virtual bool IsWindow() const = 0;
	//! Returns true if the query contains a subquery
	virtual bool HasSubquery() const = 0;
	//! Returns true if expression does not contain a group ref or col ref or parameter
	virtual bool IsScalar() const = 0;
	//! Returns true if the expression has a parameter
	virtual bool HasParameter() const = 0;

	//! Get the name of the expression
	virtual string GetName() const {
		return !alias.empty() ? alias : ToString();
	}
	//! Convert the Expression to a String
	virtual string ToString() const = 0;
	//! Print the expression to stdout
	void Print();

	//! Creates a hash value of this expression. It is important that if two expressions are identical (i.e.
	//! Expression::Equals() returns true), that their hash value is identical as well.
	virtual hash_t Hash() const = 0;
	//! Returns true if this expression is equal to another expression
	virtual bool Equals(const BaseExpression *other) const;

	static bool Equals(BaseExpression *left, BaseExpression *right) {
		if (left == right) {
			return true;
		}
		if (!left || !right) {
			return false;
		}
		return left->Equals(right);
	}
	bool operator==(const BaseExpression &rhs) {
		return this->Equals(&rhs);
	}
};

} // namespace duckdb


namespace duckdb {
class Serializer;
class Deserializer;

//!  The ParsedExpression class is a base class that can represent any expression
//!  part of a SQL statement.
/*!
 The ParsedExpression class is a base class that can represent any expression
 part of a SQL statement. This is, for example, a column reference in a SELECT
 clause, but also operators, aggregates or filters. The Expression is emitted by the parser and does not contain any
 information about bindings to the catalog or to the types. ParsedExpressions are transformed into regular Expressions
 in the Binder.
 */
class ParsedExpression : public BaseExpression {
public:
	//! Create an Expression
	ParsedExpression(ExpressionType type, ExpressionClass expression_class) : BaseExpression(type, expression_class) {
	}

public:
	bool IsAggregate() const override;
	bool IsWindow() const override;
	bool HasSubquery() const override;
	bool IsScalar() const override;
	bool HasParameter() const override;

	bool Equals(const BaseExpression *other) const override;
	hash_t Hash() const override;

	//! Create a copy of this expression
	virtual unique_ptr<ParsedExpression> Copy() const = 0;

	//! Serializes an Expression to a stand-alone binary blob
	virtual void Serialize(Serializer &serializer);
	//! Deserializes a blob back into an Expression [CAN THROW:
	//! SerializationException]
	static unique_ptr<ParsedExpression> Deserialize(Deserializer &source);

protected:
	//! Copy base Expression properties from another expression to this one,
	//! used in Copy method
	void CopyProperties(const ParsedExpression &other) {
		type = other.type;
		expression_class = other.expression_class;
		alias = other.alias;
	}
};

} // namespace duckdb


namespace duckdb {

//! A column of a table.
class ColumnDefinition {
public:
	ColumnDefinition(string name, SQLType type) : name(name), type(type) {
	}
	ColumnDefinition(string name, SQLType type, unique_ptr<ParsedExpression> default_value)
	    : name(name), type(type), default_value(move(default_value)) {
	}

	//! The name of the entry
	string name;
	//! The index of the column in the table
	idx_t oid;
	//! The type of the column
	SQLType type;
	//! The default value of the column (if any)
	unique_ptr<ParsedExpression> default_value;
};
} // namespace duckdb


namespace duckdb {

struct TableDescription {
	//! The schema of the table
	string schema;
	//! The table name of the table
	string table;
	//! The columns of the table
	vector<ColumnDefinition> columns;
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/profiler_format.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

enum class ProfilerPrintFormat : uint8_t { NONE, QUERY_TREE, JSON };

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/sql_statement.hpp
//
//
//===----------------------------------------------------------------------===//






//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/printer.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//! Printer is a static class that allows printing to logs or stdout/stderr
class Printer {
public:
	//! Print the object to stderr
	static void Print(string str);
};
} // namespace duckdb


namespace duckdb {
//! SQLStatement is the base class of any type of SQL statement.
class SQLStatement {
public:
	SQLStatement(StatementType type) : type(type){};
	virtual ~SQLStatement() {
	}

	StatementType type;
	idx_t stmt_location;
	idx_t stmt_length;
};
} // namespace duckdb


namespace duckdb {

class ClientContext;
class DuckDB;

typedef void (*warning_callback)(std::string);

//! A connection to a database. This represents a (client) connection that can
//! be used to query the database.
class Connection {
public:
	Connection(DuckDB &database);
	~Connection();

	DuckDB &db;
	unique_ptr<ClientContext> context;
	warning_callback warning_cb;

public:
	//! Returns query profiling information for the current query
	string GetProfilingInformation(ProfilerPrintFormat format = ProfilerPrintFormat::QUERY_TREE);

	//! Interrupt execution of the current query
	void Interrupt();

	//! Enable query profiling
	void EnableProfiling();
	//! Disable query profiling
	void DisableProfiling();

	void SetWarningCallback(warning_callback);

	//! Enable aggressive verification/testing of queries, should only be used in testing
	void EnableQueryVerification();

	//! Issues a query to the database and returns a QueryResult. This result can be either a StreamQueryResult or a
	//! MaterializedQueryResult. The result can be stepped through with calls to Fetch(). Note that there can only be
	//! one active StreamQueryResult per Connection object. Calling SendQuery() will invalidate any previously existing
	//! StreamQueryResult.
	unique_ptr<QueryResult> SendQuery(string query);
	//! Issues a query to the database and materializes the result (if necessary). Always returns a
	//! MaterializedQueryResult.
	unique_ptr<MaterializedQueryResult> Query(string query);
	// prepared statements
	template <typename... Args> unique_ptr<QueryResult> Query(string query, Args... args) {
		vector<Value> values;
		return QueryParamsRecursive(query, values, args...);
	}

	//! Prepare the specified query, returning a prepared statement object
	unique_ptr<PreparedStatement> Prepare(string query);

	//! Get the table info of a specific table (in the default schema), or nullptr if it cannot be found
	unique_ptr<TableDescription> TableInfo(string table_name);
	//! Get the table info of a specific table, or nullptr if it cannot be found
	unique_ptr<TableDescription> TableInfo(string schema_name, string table_name);
	//! Extract a set of SQL statements from a specific query
	vector<unique_ptr<SQLStatement>> ExtractStatements(string query);

	//! Appends a DataChunk to the specified table
	void Append(TableDescription &description, DataChunk &chunk);

private:
	unique_ptr<QueryResult> QueryParamsRecursive(string query, vector<Value> &values);

	template <typename T, typename... Args>
	unique_ptr<QueryResult> QueryParamsRecursive(string query, vector<Value> &values, T value, Args... args) {
		values.push_back(Value::CreateValue<T>(value));
		return QueryParamsRecursive(query, values, args...);
	}
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/database.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/file_system.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/file_buffer.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {
struct FileHandle;

enum class FileBufferType : uint8_t { BLOCK = 1, MANAGED_BUFFER = 2 };

//! The FileBuffer represents a buffer that can be read or written to a Direct IO FileHandle.
class FileBuffer {
public:
	//! Allocates a buffer of the specified size that is sector-aligned. bufsiz must be a multiple of
	//! FileSystemConstants::FILE_BUFFER_BLOCK_SIZE. The content in this buffer can be written to FileHandles that have
	//! been opened with DIRECT_IO on all operating systems, however, the entire buffer must be written to the file.
	//! Note that the returned size is 8 bytes less than the allocation size to account for the checksum.
	FileBuffer(FileBufferType type, uint64_t bufsiz);
	virtual ~FileBuffer();

	//! The type of the buffer
	FileBufferType type;
	//! The buffer that users can write to
	data_ptr_t buffer;
	//! The size of the portion that users can write to, this is equivalent to internal_size - BLOCK_HEADER_SIZE
	uint64_t size;

public:
	//! Read into the FileBuffer from the specified location. Automatically verifies the checksum, and throws an
	//! exception if the checksum does not match correctly.
	void Read(FileHandle &handle, uint64_t location);
	//! Write the contents of the FileBuffer to the specified location. Automatically adds a checksum of the contents of
	//! the filebuffer in front of the written data.
	void Write(FileHandle &handle, uint64_t location);

	void Clear();

	uint64_t AllocSize() {
		return internal_size;
	}

private:
	//! The pointer to the internal buffer that will be read or written, including the buffer header
	data_ptr_t internal_buffer;
	//! The aligned size as passed to the constructor. This is the size that is read or written to disk.
	uint64_t internal_size;

	//! The buffer that was actually malloc'd, i.e. the pointer that must be freed when the FileBuffer is destroyed
	data_ptr_t malloced_buffer;
};

} // namespace duckdb


#include <functional>

namespace duckdb {
class ClientContext;
class FileSystem;

struct FileHandle {
public:
	FileHandle(FileSystem &file_system, string path) : file_system(file_system), path(path) {
	}
	FileHandle(const FileHandle &) = delete;
	virtual ~FileHandle() {
	}

	void Read(void *buffer, idx_t nr_bytes, idx_t location);
	void Write(void *buffer, idx_t nr_bytes, idx_t location);
	void Sync();
	void Truncate(int64_t new_size);

protected:
	virtual void Close() = 0;

public:
	FileSystem &file_system;
	string path;
};

enum class FileLockType : uint8_t { NO_LOCK = 0, READ_LOCK = 1, WRITE_LOCK = 2 };

class FileFlags {
public:
	//! Open file with read access
	static constexpr uint8_t READ = 1 << 0;
	//! Open file with read/write access
	static constexpr uint8_t WRITE = 1 << 1;
	//! Use direct IO when reading/writing to the file
	static constexpr uint8_t DIRECT_IO = 1 << 2;
	//! Create file if not exists, can only be used together with WRITE
	static constexpr uint8_t CREATE = 1 << 3;
	//! Open file in append mode
	static constexpr uint8_t APPEND = 1 << 4;
};

class FileSystem {
public:
	virtual ~FileSystem() {
	}

public:
	static FileSystem &GetFileSystem(ClientContext &context);

	virtual unique_ptr<FileHandle> OpenFile(const char *path, uint8_t flags, FileLockType lock = FileLockType::NO_LOCK);
	unique_ptr<FileHandle> OpenFile(string &path, uint8_t flags, FileLockType lock = FileLockType::NO_LOCK) {
		return OpenFile(path.c_str(), flags, lock);
	}
	//! Read exactly nr_bytes from the specified location in the file. Fails if nr_bytes could not be read. This is
	//! equivalent to calling SetFilePointer(location) followed by calling Read().
	virtual void Read(FileHandle &handle, void *buffer, int64_t nr_bytes, idx_t location);
	//! Write exactly nr_bytes to the specified location in the file. Fails if nr_bytes could not be read. This is
	//! equivalent to calling SetFilePointer(location) followed by calling Write().
	virtual void Write(FileHandle &handle, void *buffer, int64_t nr_bytes, idx_t location);
	//! Read nr_bytes from the specified file into the buffer, moving the file pointer forward by nr_bytes. Returns the
	//! amount of bytes read.
	virtual int64_t Read(FileHandle &handle, void *buffer, int64_t nr_bytes);
	//! Write nr_bytes from the buffer into the file, moving the file pointer forward by nr_bytes.
	virtual int64_t Write(FileHandle &handle, void *buffer, int64_t nr_bytes);

	//! Returns the file size of a file handle, returns -1 on error
	virtual int64_t GetFileSize(FileHandle &handle);
	//! Truncate a file to a maximum size of new_size, new_size should be smaller than or equal to the current size of
	//! the file
	virtual void Truncate(FileHandle &handle, int64_t new_size);

	//! Check if a directory exists
	virtual bool DirectoryExists(const string &directory);
	//! Create a directory if it does not exist
	virtual void CreateDirectory(const string &directory);
	//! Recursively remove a directory and all files in it
	virtual void RemoveDirectory(const string &directory);
	//! List files in a directory, invoking the callback method for each one
	virtual bool ListFiles(const string &directory, std::function<void(string)> callback);
	//! Move a file from source path to the target, StorageManager relies on this being an atomic action for ACID
	//! properties
	virtual void MoveFile(const string &source, const string &target);
	//! Check if a file exists
	virtual bool FileExists(const string &filename);
	//! Remove a file from disk
	virtual void RemoveFile(const string &filename);
	//! Path separator for the current file system
	virtual string PathSeparator();
	//! Join two paths together
	virtual string JoinPath(const string &a, const string &path);
	//! Sync a file handle to disk
	virtual void FileSync(FileHandle &handle);

private:
	//! Set the file pointer of a file handle to a specified location. Reads and writes will happen from this location
	void SetFilePointer(FileHandle &handle, idx_t location);
};

} // namespace duckdb


namespace duckdb {
class StorageManager;
class Catalog;
class TransactionManager;
class ConnectionManager;
class FileSystem;

enum class AccessMode : uint8_t { UNDEFINED = 0, AUTOMATIC = 1, READ_ONLY = 2, READ_WRITE = 3 };

// this is optional and only used in tests at the moment
struct DBConfig {
	friend class DuckDB;
	friend class StorageManager;

public:
	~DBConfig();

	//! Access mode of the database (AUTOMATIC, READ_ONLY or READ_WRITE)
	AccessMode access_mode = AccessMode::AUTOMATIC;
	// Checkpoint when WAL reaches this size
	idx_t checkpoint_wal_size = 1 << 20;
	//! Whether or not to use Direct IO, bypassing operating system buffers
	bool use_direct_io = false;
	//! The FileSystem to use, can be overwritten to allow for injecting custom file systems for testing purposes (e.g.
	//! RamFS or something similar)
	unique_ptr<FileSystem> file_system;
	//! The maximum memory used by the database system (in bytes). Default: Infinite
	idx_t maximum_memory = (idx_t)-1;
	//! Whether or not to create and use a temporary directory to store intermediates that do not fit in memory
	bool use_temporary_directory = true;
	//! Directory to store temporary structures that do not fit in memory
	string temporary_directory;

private:
	// FIXME: don't set this as a user: used internally (only for now)
	bool checkpoint_only = false;
};

//! The database object. This object holds the catalog and all the
//! database-specific meta information.
class Connection;
class DuckDB {
public:
	DuckDB(const char *path = nullptr, DBConfig *config = nullptr);
	DuckDB(const string &path, DBConfig *config = nullptr);

	~DuckDB();

	unique_ptr<FileSystem> file_system;
	unique_ptr<StorageManager> storage;
	unique_ptr<Catalog> catalog;
	unique_ptr<TransactionManager> transaction_manager;
	unique_ptr<ConnectionManager> connection_manager;

	AccessMode access_mode;
	bool use_direct_io;
	bool checkpoint_only;
	idx_t checkpoint_wal_size;
	idx_t maximum_memory;
	string temporary_directory;

private:
	void Configure(DBConfig &config);
};

} // namespace duckdb


//===----------------------------------------------------------------------===//
//
//                         DuckDB
//
// duckdb.h
//
// Author: Mark Raasveldt
//
//===----------------------------------------------------------------------===//



#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef uint64_t idx_t;

typedef enum DUCKDB_TYPE {
	DUCKDB_TYPE_INVALID = 0,
	// bool
	DUCKDB_TYPE_BOOLEAN,
	// int8_t
	DUCKDB_TYPE_TINYINT,
	// int16_t
	DUCKDB_TYPE_SMALLINT,
	// int32_t
	DUCKDB_TYPE_INTEGER,
	// int64_t
	DUCKDB_TYPE_BIGINT,
	// float
	DUCKDB_TYPE_FLOAT,
	// double
	DUCKDB_TYPE_DOUBLE,
	// duckdb_timestamp
	DUCKDB_TYPE_TIMESTAMP,
	// duckdb_date
	DUCKDB_TYPE_DATE,
	// duckdb_time
	DUCKDB_TYPE_TIME,
	// const char*
	DUCKDB_TYPE_VARCHAR
} duckdb_type;

typedef struct {
	int32_t year;
	int8_t month;
	int8_t day;
} duckdb_date;

typedef struct {
	int8_t hour;
	int8_t min;
	int8_t sec;
	int16_t msec;
} duckdb_time;

typedef struct {
	duckdb_date date;
	duckdb_time time;
} duckdb_timestamp;

typedef struct {
	void *data;
	bool *nullmask;
	duckdb_type type;
	char *name;
} duckdb_column;

typedef struct {
	idx_t column_count;
	idx_t row_count;
	duckdb_column *columns;
	char *error_message;
} duckdb_result;

// typedef struct {
// 	void *data;
// 	bool *nullmask;
// } duckdb_column_data;

// typedef struct {
// 	int column_count;
// 	int count;
// 	duckdb_column_data *columns;
// } duckdb_chunk;

typedef void *duckdb_database;
typedef void *duckdb_connection;
typedef void *duckdb_prepared_statement;

typedef enum { DuckDBSuccess = 0, DuckDBError = 1 } duckdb_state;

//! Opens a database file at the given path (nullptr for in-memory). Returns DuckDBSuccess on success, or DuckDBError on
//! failure. [OUT: database]
duckdb_state duckdb_open(const char *path, duckdb_database *out_database);
//! Closes the database.
void duckdb_close(duckdb_database *database);

//! Creates a connection to the specified database. [OUT: connection]
duckdb_state duckdb_connect(duckdb_database database, duckdb_connection *out_connection);
//! Closes the specified connection handle
void duckdb_disconnect(duckdb_connection *connection);

//! Executes the specified SQL query in the specified connection handle. [OUT: result descriptor]
duckdb_state duckdb_query(duckdb_connection connection, const char *query, duckdb_result *out_result);
//! Destroys the specified result
void duckdb_destroy_result(duckdb_result *result);

// SAFE fetch functions
// These functions will perform conversions if necessary. On failure (e.g. if conversion cannot be performed) a special
// value is returned.

//! Converts the specified value to a bool. Returns false on failure or NULL.
bool duckdb_value_boolean(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to an int8_t. Returns 0 on failure or NULL.
int8_t duckdb_value_int8(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to an int16_t. Returns 0 on failure or NULL.
int16_t duckdb_value_int16(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to an int64_t. Returns 0 on failure or NULL.
int32_t duckdb_value_int32(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to an int64_t. Returns 0 on failure or NULL.
int64_t duckdb_value_int64(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to a float. Returns 0.0 on failure or NULL.
float duckdb_value_float(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to a double. Returns 0.0 on failure or NULL.
double duckdb_value_double(duckdb_result *result, idx_t col, idx_t row);
//! Converts the specified value to a string. Returns nullptr on failure or NULL. The result must be freed with free.
char *duckdb_value_varchar(duckdb_result *result, idx_t col, idx_t row);

// Prepared Statements

//! prepares the specified SQL query in the specified connection handle. [OUT: prepared statement descriptor]
duckdb_state duckdb_prepare(duckdb_connection connection, const char *query,
                            duckdb_prepared_statement *out_prepared_statement);

duckdb_state duckdb_nparams(duckdb_prepared_statement prepared_statement, idx_t *nparams_out);

//! binds parameters to prepared statement
duckdb_state duckdb_bind_boolean(duckdb_prepared_statement prepared_statement, idx_t param_idx, bool val);
duckdb_state duckdb_bind_int8(duckdb_prepared_statement prepared_statement, idx_t param_idx, int8_t val);
duckdb_state duckdb_bind_int16(duckdb_prepared_statement prepared_statement, idx_t param_idx, int16_t val);
duckdb_state duckdb_bind_int32(duckdb_prepared_statement prepared_statement, idx_t param_idx, int32_t val);
duckdb_state duckdb_bind_int64(duckdb_prepared_statement prepared_statement, idx_t param_idx, int64_t val);
duckdb_state duckdb_bind_float(duckdb_prepared_statement prepared_statement, idx_t param_idx, float val);
duckdb_state duckdb_bind_double(duckdb_prepared_statement prepared_statement, idx_t param_idx, double val);
duckdb_state duckdb_bind_varchar(duckdb_prepared_statement prepared_statement, idx_t param_idx, const char *val);
duckdb_state duckdb_bind_null(duckdb_prepared_statement prepared_statement, idx_t param_idx);

//! Executes the prepared statements with currently bound parameters
duckdb_state duckdb_execute_prepared(duckdb_prepared_statement prepared_statement, duckdb_result *out_result);

//! Destroys the specified prepared statement descriptor
void duckdb_destroy_prepare(duckdb_prepared_statement *prepared_statement);

#ifdef __cplusplus
};
#endif
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/date.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//! The Date class is a static class that holds helper functions for the Date
//! type.
class Date {
public:
	//! Convert a string in the format "YYYY-MM-DD" to a date object
	static date_t FromString(string str);
	//! Convert a string in the format "YYYY-MM-DD" to a date object
	static date_t FromCString(const char *str);
	//! Convert a date object to a string in the format "YYYY-MM-DD"
	static string ToString(date_t date);

	//! Create a string "YYYY-MM-DD" from a specified (year, month, day)
	//! combination
	static string Format(int32_t year, int32_t month, int32_t day);

	//! Extract the year, month and day from a given date object
	static void Convert(date_t date, int32_t &out_year, int32_t &out_month, int32_t &out_day);
	//! Create a Date object from a specified (year, month, day) combination
	static date_t FromDate(int32_t year, int32_t month, int32_t day);

	//! Returns true if (year) is a leap year, and false otherwise
	static bool IsLeapYear(int32_t year);

	//! Returns true if the specified (year, month, day) combination is a valid
	//! date
	static bool IsValidDay(int32_t year, int32_t month, int32_t day);

	//! Extract the epoch from the date (seconds since 1970-01-01)
	static int64_t Epoch(date_t date);
	//! Convert the epoch (seconds since 1970-01-01) to a date_t
	static date_t EpochToDate(int64_t epoch);
	//! Extract year of a date entry
	static int32_t ExtractYear(date_t date);
	//! Extract month of a date entry
	static int32_t ExtractMonth(date_t date);
	//! Extract day of a date entry
	static int32_t ExtractDay(date_t date);
	//! Extract the day of the week (1-7)
	static int32_t ExtractISODayOfTheWeek(date_t date);
	//! Extract the day of the year
	static int32_t ExtractDayOfTheYear(date_t date);
	//! Extract the week number
	static int32_t ExtractWeekNumber(date_t date);
	//! Returns the date of the monday of the current week.
	static date_t GetMondayOfCurrentWeek(date_t date);
};
} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/timestamp.hpp
//
//
//===----------------------------------------------------------------------===//





#include <chrono>  // chrono::system_clock
#include <ctime>   // localtime
#include <iomanip> // put_time
#include <sstream> // stringstream
#include <string>  // string

namespace duckdb {

struct Interval {
	int64_t time;
	int32_t days;   //! days, after time for alignment
	int32_t months; //! months after time for alignment
};

struct timestamp_struct {
	int32_t year;
	int8_t month;
	int8_t day;
	int8_t hour;
	int8_t min;
	int8_t sec;
	int16_t msec;
};
//! The Timestamp class is a static class that holds helper functions for the Timestamp
//! type.
class Timestamp {
public:
	//! Convert a string in the format "YYYY-MM-DD hh:mm:ss" to a timestamp object
	static timestamp_t FromString(string str);
	//! Convert a date object to a string in the format "YYYY-MM-DDThh:mm:ssZ"
	static string ToString(timestamp_t timestamp);

	static date_t GetDate(timestamp_t timestamp);

	static dtime_t GetTime(timestamp_t timestamp);
	//! Create a Timestamp object from a specified (date, time) combination
	static timestamp_t FromDatetime(date_t date, dtime_t time);
	//! Extract the date and time from a given timestamp object
	static void Convert(timestamp_t date, date_t &out_date, dtime_t &out_time);
	//! Returns current timestamp
	static timestamp_t GetCurrentTimestamp();
	//! Gets the timestamp which correspondes to the difference between the given ones
	static Interval GetDifference(timestamp_t timestamp_a, timestamp_t timestamp_b);

	static timestamp_struct IntervalToTimestamp(Interval &interval);

	// Unix epoch: milliseconds since 1970
	static int64_t GetEpoch(timestamp_t timestamp);
	// Seconds including fractional part multiplied by 1000
	static int64_t GetMilliseconds(timestamp_t timestamp);
	static int64_t GetSeconds(timestamp_t timestamp);
	static int64_t GetMinutes(timestamp_t timestamp);
	static int64_t GetHours(timestamp_t timestamp);
};
} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/appender.hpp
//
//
//===----------------------------------------------------------------------===//






namespace duckdb {

class ClientContext;
class DuckDB;
class TableCatalogEntry;
class Connection;

//! The Appender class can be used to append elements to a table.
class Appender {
	//! A reference to a database connection that created this appender
	Connection &con;
	//! The table description (including column names)
	unique_ptr<TableDescription> description;
	//! Internal chunk used for appends
	DataChunk chunk;
	//! The current column to append to
	idx_t column = 0;
	//! Message explaining why the Appender is invalidated (if any)
	string invalidated_msg;

public:
	Appender(Connection &con, string schema_name, string table_name);
	Appender(Connection &con, string table_name);
	~Appender();

	//! Begins a new row append, after calling this the other AppendX() functions
	//! should be called the correct amount of times. After that,
	//! EndRow() should be called.
	void BeginRow();
	//! Finishes appending the current row.
	void EndRow();

	// Append functions
	template <class T> void Append(T value) {
		throw Exception("Undefined type for Appender::Append!");
	}

	// prepared statements
	template <typename... Args> void AppendRow(Args... args) {
		BeginRow();
		AppendRowRecursive(args...);
	}

	//! Commit the changes made by the appender.
	void Flush();
	//! Flush the changes made by the appender and close it. The appender cannot be used after this point
	void Close();

	//! Obtain a reference to the internal vector that is used to append to the table
	DataChunk &GetAppendChunk() {
		return chunk;
	}

	idx_t CurrentColumn() {
		return column;
	}

	void Invalidate(string msg, bool close = true);

private:
	//! Invalidate the appender with a specific message and throw an exception with the same message
	void InvalidateException(string msg);

	template <class T> void AppendValueInternal(T value);
	template <class SRC, class DST> void AppendValueInternal(Vector &vector, SRC input);

	void CheckInvalidated();

	void AppendRowRecursive() {
		EndRow();
	}

	template <typename T, typename... Args> void AppendRowRecursive(T value, Args... args) {
		Append<T>(value);
		AppendRowRecursive(args...);
	}

	void AppendValue(Value value);
};

template <> void Appender::Append(bool value);
template <> void Appender::Append(int8_t value);
template <> void Appender::Append(int16_t value);
template <> void Appender::Append(int32_t value);
template <> void Appender::Append(int64_t value);
template <> void Appender::Append(double value);
template <> void Appender::Append(const char *value);
template <> void Appender::Append(Value value);
template <> void Appender::Append(std::nullptr_t value);

} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/client_context.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_set.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/catalog_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Catalog Types
//===--------------------------------------------------------------------===//
enum class CatalogType : uint8_t {
	INVALID = 0,
	TABLE = 1,
	SCHEMA = 2,
	TABLE_FUNCTION = 3,
	SCALAR_FUNCTION = 4,
	AGGREGATE_FUNCTION = 5,
	VIEW = 6,
	INDEX = 7,
	PREPARED_STATEMENT = 8,
	SEQUENCE = 9,

	UPDATED_ENTRY = 50,
	DELETED_ENTRY = 51,
};

string CatalogTypeToString(CatalogType type);

} // namespace duckdb


#include <memory>

namespace duckdb {
struct AlterInfo;
class Catalog;
class CatalogSet;
class ClientContext;

//! Abstract base class of an entry in the catalog
class CatalogEntry {
public:
	CatalogEntry(CatalogType type, Catalog *catalog, string name)
	    : type(type), catalog(catalog), set(nullptr), name(name), deleted(false), temporary(false), parent(nullptr) {
	}
	virtual ~CatalogEntry();

	virtual unique_ptr<CatalogEntry> AlterEntry(ClientContext &context, AlterInfo *info) {
		throw CatalogException("Unsupported alter type for catalog entry!");
	}

	virtual unique_ptr<CatalogEntry> Copy(ClientContext &context) {
		throw CatalogException("Unsupported copy type for catalog entry!");
	}
	//! The type of this catalog entry
	CatalogType type;
	//! Reference to the catalog this entry belongs to
	Catalog *catalog;
	//! Reference to the catalog set this entry is stored in
	CatalogSet *set;
	//! The name of the entry
	string name;
	//! Whether or not the object is deleted
	bool deleted;
	//! Whether or not the object is temporary and should not be added to the WAL
	bool temporary;
	//! Timestamp at which the catalog entry was created
	transaction_t timestamp;
	//! Child entry
	unique_ptr<CatalogEntry> child;
	//! Parent entry (the node that owns this node)
	CatalogEntry *parent;
};
} // namespace duckdb



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/unordered_set.hpp
//
//
//===----------------------------------------------------------------------===//



#include <unordered_set>

namespace duckdb {
using std::unordered_set;
}


#include <functional>
#include <memory>
#include <mutex>

namespace duckdb {
struct AlterInfo;

class Transaction;

typedef unordered_map<CatalogSet *, std::unique_lock<std::mutex>> set_lock_map_t;

//! The Catalog Set stores (key, value) map of a set of AbstractCatalogEntries
class CatalogSet {
	friend class DependencyManager;

public:
	CatalogSet(Catalog &catalog);

	//! Create an entry in the catalog set. Returns whether or not it was
	//! successful.
	bool CreateEntry(Transaction &transaction, const string &name, unique_ptr<CatalogEntry> value,
	                 unordered_set<CatalogEntry *> &dependencies);

	bool AlterEntry(ClientContext &context, const string &name, AlterInfo *alter_info);

	bool DropEntry(Transaction &transaction, const string &name, bool cascade);
	//! Returns the entry with the specified name
	CatalogEntry *GetEntry(Transaction &transaction, const string &name);
	//! Returns the root entry with the specified name regardless of transaction (or nullptr if there are none)
	CatalogEntry *GetRootEntry(const string &name);

	//! Rollback <entry> to be the currently valid entry for a certain catalog
	//! entry
	void Undo(CatalogEntry *entry);

	//! Scan the catalog set, invoking the callback method for every entry
	template <class T> void Scan(Transaction &transaction, T &&callback) {
		// lock the catalog set
		std::lock_guard<std::mutex> lock(catalog_lock);
		for (auto &kv : data) {
			auto entry = kv.second.get();
			entry = GetEntryForTransaction(transaction, entry);
			if (!entry->deleted) {
				callback(entry);
			}
		}
	}

	static bool HasConflict(Transaction &transaction, CatalogEntry &current);

private:
	//! Drops an entry from the catalog set; must hold the catalog_lock to
	//! safely call this
	void DropEntryInternal(Transaction &transaction, CatalogEntry &entry, bool cascade, set_lock_map_t &lock_set);
	//! Given a root entry, gets the entry valid for this transaction
	CatalogEntry *GetEntryForTransaction(Transaction &transaction, CatalogEntry *current);

	Catalog &catalog;
	//! The catalog lock is used to make changes to the data
	std::mutex catalog_lock;
	//! The set of entries present in the CatalogSet.
	unordered_map<string, unique_ptr<CatalogEntry>> data;
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry/schema_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//






namespace duckdb {
class ClientContext;

class StandardEntry;
class TableCatalogEntry;
class TableFunctionCatalogEntry;
class SequenceCatalogEntry;

enum class OnCreateConflict : uint8_t;

struct AlterTableInfo;
struct CreateIndexInfo;
struct CreateTableFunctionInfo;
struct CreateFunctionInfo;
struct CreateViewInfo;
struct BoundCreateTableInfo;
struct CreateSequenceInfo;
struct CreateSchemaInfo;
struct CreateTableFunctionInfo;
struct DropInfo;

//! A schema in the catalog
class SchemaCatalogEntry : public CatalogEntry {
public:
	SchemaCatalogEntry(Catalog *catalog, string name);

	//! The catalog set holding the tables
	CatalogSet tables;
	//! The catalog set holding the indexes
	CatalogSet indexes;
	//! The catalog set holding the table functions
	CatalogSet table_functions;
	//! The catalog set holding the scalar and aggregate functions
	CatalogSet functions;
	//! The catalog set holding the sequences
	CatalogSet sequences;

public:
	//! Creates a table with the given name in the schema
	CatalogEntry *CreateTable(ClientContext &context, BoundCreateTableInfo *info);
	//! Creates a view with the given name in the schema
	CatalogEntry *CreateView(ClientContext &context, CreateViewInfo *info);
	//! Creates a sequence with the given name in the schema
	CatalogEntry *CreateSequence(ClientContext &context, CreateSequenceInfo *info);
	//! Creates an index with the given name in the schema
	CatalogEntry *CreateIndex(ClientContext &context, CreateIndexInfo *info);
	//! Create a table function within the given schema
	CatalogEntry *CreateTableFunction(ClientContext &context, CreateTableFunctionInfo *info);
	//! Create a scalar or aggregate function within the given schema
	CatalogEntry *CreateFunction(ClientContext &context, CreateFunctionInfo *info);

	//! Drops an entry from the schema
	void DropEntry(ClientContext &context, DropInfo *info);

	//! Alters a table
	void AlterTable(ClientContext &context, AlterTableInfo *info);

	//! Gets a catalog entry from the given catalog set matching the given name
	CatalogEntry *GetEntry(ClientContext &context, CatalogType type, const string &name, bool if_exists);

	//! Serialize the meta information of the SchemaCatalogEntry a serializer
	virtual void Serialize(Serializer &serializer);
	//! Deserializes to a CreateSchemaInfo
	static unique_ptr<CreateSchemaInfo> Deserialize(Deserializer &source);

private:
	//! Add a catalog entry to this schema
	CatalogEntry *AddEntry(ClientContext &context, unique_ptr<StandardEntry> entry, OnCreateConflict on_conflict);
	//! Add a catalog entry to this schema
	CatalogEntry *AddEntry(ClientContext &context, unique_ptr<StandardEntry> entry, OnCreateConflict on_conflict,
	                       unordered_set<CatalogEntry *> dependencies);

	//! Get the catalog set for the specified type
	CatalogSet &GetCatalogSet(CatalogType type);
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/execution_context.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/physical_operator.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog.hpp
//
//
//===----------------------------------------------------------------------===//





//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/dependency_manager.hpp
//
//
//===----------------------------------------------------------------------===//






#include <mutex>

namespace duckdb {
class Catalog;
class Transaction;

//! The DependencyManager is in charge of managing dependencies between catalog entries
class DependencyManager {
	friend class CatalogSet;

public:
	DependencyManager(Catalog &catalog);

	//! Erase the object from the DependencyManager; this should only happen when the object itself is destroyed
	void EraseObject(CatalogEntry *object);
	// //! Clear all the dependencies of all entries in the catalog set
	void ClearDependencies(CatalogSet &set);

private:
	Catalog &catalog;
	//! Map of objects that DEPEND on [object], i.e. [object] can only be deleted when all entries in the dependency map
	//! are deleted.
	unordered_map<CatalogEntry *, unordered_set<CatalogEntry *>> dependents_map;
	//! Map of objects that the source object DEPENDS on, i.e. when any of the entries in the vector perform a CASCADE
	//! drop then [object] is deleted as wel
	unordered_map<CatalogEntry *, unordered_set<CatalogEntry *>> dependencies_map;

private:
	void AddObject(Transaction &transaction, CatalogEntry *object, unordered_set<CatalogEntry *> &dependencies);
	void DropObject(Transaction &transaction, CatalogEntry *object, bool cascade, set_lock_map_t &lock_set);
	void AlterObject(Transaction &transaction, CatalogEntry *old_obj, CatalogEntry *new_obj);
	void EraseObjectInternal(CatalogEntry *object);
};
} // namespace duckdb


#include <mutex>

namespace duckdb {
struct CreateSchemaInfo;
struct DropInfo;
struct BoundCreateTableInfo;
struct AlterTableInfo;
struct CreateTableFunctionInfo;
struct CreateFunctionInfo;
struct CreateViewInfo;
struct CreateSequenceInfo;

class ClientContext;
class Transaction;

class AggregateFunctionCatalogEntry;
class SchemaCatalogEntry;
class TableCatalogEntry;
class SequenceCatalogEntry;
class TableFunctionCatalogEntry;
class StorageManager;

//! The Catalog object represents the catalog of the database.
class Catalog {
public:
	Catalog(StorageManager &storage);

	//! Reference to the storage manager
	StorageManager &storage;
	//! The catalog set holding the schemas
	CatalogSet schemas;
	//! The DependencyManager manages dependencies between different catalog objects
	DependencyManager dependency_manager;
	//! Write lock for the catalog
	std::mutex write_lock;

public:
	//! Get the ClientContext from the Catalog
	static Catalog &GetCatalog(ClientContext &context);

	//! Creates a schema in the catalog.
	CatalogEntry *CreateSchema(ClientContext &context, CreateSchemaInfo *info);
	//! Creates a table in the catalog.
	CatalogEntry *CreateTable(ClientContext &context, BoundCreateTableInfo *info);
	//! Create a table function in the catalog
	CatalogEntry *CreateTableFunction(ClientContext &context, CreateTableFunctionInfo *info);
	//! Create a scalar or aggregate function in the catalog
	CatalogEntry *CreateFunction(ClientContext &context, CreateFunctionInfo *info);
	//! Creates a table in the catalog.
	CatalogEntry *CreateView(ClientContext &context, CreateViewInfo *info);
	//! Creates a table in the catalog.
	CatalogEntry *CreateSequence(ClientContext &context, CreateSequenceInfo *info);

	//! Drops an entry from the catalog
	void DropEntry(ClientContext &context, DropInfo *info);

	//! Returns the schema object with the specified name, or throws an exception if it does not exist
	SchemaCatalogEntry *GetSchema(ClientContext &context, const string &name = DEFAULT_SCHEMA);
	//! Gets the "schema.name" entry of the specified type, if if_exists=true returns nullptr if entry does not exist,
	//! otherwise an exception is thrown
	CatalogEntry *GetEntry(ClientContext &context, CatalogType type, string schema, const string &name,
	                       bool if_exists = false);
	template <class T>
	T *GetEntry(ClientContext &context, string schema_name, const string &name, bool if_exists = false);

	//! Alter an existing table in the catalog.
	void AlterTable(ClientContext &context, AlterTableInfo *info);

	//! Parse the (optional) schema and a name from a string in the format of e.g. "schema"."table"; if there is no dot
	//! the schema will be set to DEFAULT_SCHEMA
	static void ParseRangeVar(string input, string &schema, string &name);

private:
	void DropSchema(ClientContext &context, DropInfo *info);
};

template <>
TableCatalogEntry *Catalog::GetEntry(ClientContext &context, string schema_name, const string &name, bool if_exists);
template <>
SequenceCatalogEntry *Catalog::GetEntry(ClientContext &context, string schema_name, const string &name, bool if_exists);
template <>
TableFunctionCatalogEntry *Catalog::GetEntry(ClientContext &context, string schema_name, const string &name,
                                             bool if_exists);
template <>
AggregateFunctionCatalogEntry *Catalog::GetEntry(ClientContext &context, string schema_name, const string &name,
                                                 bool if_exists);

} // namespace duckdb


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/physical_operator_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Physical Operator Types
//===--------------------------------------------------------------------===//
enum class PhysicalOperatorType : uint8_t {
	INVALID,
	LEAF,
	ORDER_BY,
	LIMIT,
	TOP_N,
	AGGREGATE,
	WINDOW,
	UNNEST,
	DISTINCT,
	SIMPLE_AGGREGATE,
	HASH_GROUP_BY,
	SORT_GROUP_BY,
	FILTER,
	PROJECTION,
	COPY_FROM_FILE,
	COPY_TO_FILE,
	TABLE_FUNCTION,
	// -----------------------------
	// Scans
	// -----------------------------
	DUMMY_SCAN,
	SEQ_SCAN,
	INDEX_SCAN,
	CHUNK_SCAN,
	DELIM_SCAN,
	EXTERNAL_FILE_SCAN,
	QUERY_DERIVED_SCAN,
	EXPRESSION_SCAN,
	// -----------------------------
	// Joins
	// -----------------------------
	BLOCKWISE_NL_JOIN,
	NESTED_LOOP_JOIN,
	HASH_JOIN,
	CROSS_PRODUCT,
	PIECEWISE_MERGE_JOIN,
	DELIM_JOIN,

	// -----------------------------
	// SetOps
	// -----------------------------
	UNION,
	RECURSIVE_CTE,

	// -----------------------------
	// Updates
	// -----------------------------
	INSERT,
	INSERT_SELECT,
	DELETE,
	UPDATE,
	EXPORT_EXTERNAL_FILE,

	// -----------------------------
	// Schema
	// -----------------------------
	CREATE,
	CREATE_INDEX,
	ALTER,
	CREATE_SEQUENCE,
	CREATE_VIEW,
	CREATE_SCHEMA,
	DROP,
	PRAGMA,
	TRANSACTION,

	// -----------------------------
	// Helpers
	// -----------------------------
	PRUNE_COLUMNS,
	EXPLAIN,
	EMPTY_RESULT,
	EXECUTE,
	PREPARE,
	VACUUM
};

string PhysicalOperatorToString(PhysicalOperatorType type);

} // namespace duckdb


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/statement/select_statement.hpp
//
//
//===----------------------------------------------------------------------===//





//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/query_node.hpp
//
//
//===----------------------------------------------------------------------===//





//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/serializer.hpp
//
//
//===----------------------------------------------------------------------===//






namespace duckdb {

//! The Serialize class is a base class that can be used to serializing objects into a binary buffer
class Serializer {
public:
	virtual ~Serializer() {
	}

	virtual void WriteData(const_data_ptr_t buffer, idx_t write_size) = 0;

	template <class T> void Write(T element) {
		WriteData((const_data_ptr_t)&element, sizeof(T));
	}

	void WriteString(const string &val) {
		assert(val.size() <= std::numeric_limits<uint32_t>::max());
		Write<uint32_t>((uint32_t)val.size());
		if (val.size() > 0) {
			WriteData((const_data_ptr_t)val.c_str(), val.size());
		}
	}

	template <class T> void WriteList(vector<unique_ptr<T>> &list) {
		assert(list.size() <= std::numeric_limits<uint32_t>::max());
		Write<uint32_t>((uint32_t)list.size());
		for (auto &child : list) {
			child->Serialize(*this);
		}
	}

	template <class T> void WriteOptional(unique_ptr<T> &element) {
		Write<bool>(element ? true : false);
		if (element) {
			element->Serialize(*this);
		}
	}
};

//! The Deserializer class assists in deserializing a binary blob back into an
//! object
class Deserializer {
public:
	virtual ~Deserializer() {
	}

	//! Reads [read_size] bytes into the buffer
	virtual void ReadData(data_ptr_t buffer, idx_t read_size) = 0;

	template <class T> T Read() {
		T value;
		ReadData((data_ptr_t)&value, sizeof(T));
		return value;
	}

	template <class T> void ReadList(vector<unique_ptr<T>> &list) {
		auto select_count = Read<uint32_t>();
		for (uint32_t i = 0; i < select_count; i++) {
			auto child = T::Deserialize(*this);
			list.push_back(move(child));
		}
	}

	template <class T> unique_ptr<T> ReadOptional() {
		auto has_entry = Read<bool>();
		if (has_entry) {
			return T::Deserialize(*this);
		}
		return nullptr;
	}
};

template <> string Deserializer::Read();

} // namespace duckdb



namespace duckdb {

enum QueryNodeType : uint8_t { SELECT_NODE = 1, SET_OPERATION_NODE = 2, BOUND_SUBQUERY_NODE = 3, RECURSIVE_CTE_NODE = 4 };

//! Single node in ORDER BY statement
struct OrderByNode {
	OrderByNode() {
	}
	OrderByNode(OrderType type, unique_ptr<ParsedExpression> expression) : type(type), expression(move(expression)) {
	}

	//! Sort order, ASC or DESC
	OrderType type;
	//! Expression to order by
	unique_ptr<ParsedExpression> expression;
};

class QueryNode {
public:
	QueryNode(QueryNodeType type) : type(type) {
	}
	virtual ~QueryNode() {
	}

	//! The type of the query node, either SetOperation or Select
	QueryNodeType type;
	//! DISTINCT or not
	bool select_distinct = false;
	//! List of order nodes
	vector<OrderByNode> orders;
	//! LIMIT count
	unique_ptr<ParsedExpression> limit;
	//! OFFSET
	unique_ptr<ParsedExpression> offset;

	virtual const vector<unique_ptr<ParsedExpression>> &GetSelectList() const = 0;

public:
	virtual bool Equals(const QueryNode *other) const;

	//! Create a copy of this QueryNode
	virtual unique_ptr<QueryNode> Copy() = 0;
	//! Serializes a QueryNode to a stand-alone binary blob
	virtual void Serialize(Serializer &serializer);
	//! Deserializes a blob back into a QueryNode, returns nullptr if
	//! deserialization is not possible
	static unique_ptr<QueryNode> Deserialize(Deserializer &source);

protected:
	void CopyProperties(QueryNode &other);
};

}; // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/query_node/select_node.hpp
//
//
//===----------------------------------------------------------------------===//






//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/tableref.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/tableref_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Table Reference Types
//===--------------------------------------------------------------------===//
enum class TableReferenceType : uint8_t {
	INVALID = 0,         // invalid table reference type
	BASE_TABLE = 1,      // base table reference
	SUBQUERY = 2,        // output of a subquery
	JOIN = 3,            // output of join
	CROSS_PRODUCT = 4,   // out of cartesian product
	TABLE_FUNCTION = 5,  // table producing function
	EXPRESSION_LIST = 6, // expression list
	CTE = 7,             // Recursive CTE
	EMPTY = 8            // placeholder for empty FROM
};

} // namespace duckdb


namespace duckdb {
class Deserializer;
class Serializer;

//! Represents a generic expression that returns a table.
class TableRef {
public:
	TableRef(TableReferenceType type) : type(type) {
	}
	virtual ~TableRef() {
	}

	TableReferenceType type;
	string alias;

public:
	//! Convert the object to a string
	virtual string ToString() const {
		return string();
	}
	void Print();

	virtual bool Equals(const TableRef *other) const {
		return other && type == other->type && alias == other->alias;
	}

	virtual unique_ptr<TableRef> Copy() = 0;

	//! Serializes a TableRef to a stand-alone binary blob
	virtual void Serialize(Serializer &serializer);
	//! Deserializes a blob back into a TableRef
	static unique_ptr<TableRef> Deserialize(Deserializer &source);
};
} // namespace duckdb


namespace duckdb {

//! SelectNode represents a standard SELECT statement
class SelectNode : public QueryNode {
public:
	SelectNode() : QueryNode(QueryNodeType::SELECT_NODE) {
	}

	//! The projection list
	vector<unique_ptr<ParsedExpression>> select_list;
	//! The FROM clause
	unique_ptr<TableRef> from_table;
	//! The WHERE clause
	unique_ptr<ParsedExpression> where_clause;
	//! list of groups
	vector<unique_ptr<ParsedExpression>> groups;
	//! list of distinct on targets
	vector<unique_ptr<ParsedExpression>> distinct_on_targets;
	//! HAVING clause
	unique_ptr<ParsedExpression> having;

	const vector<unique_ptr<ParsedExpression>> &GetSelectList() const override {
		return select_list;
	}

public:
	bool Equals(const QueryNode *other) const override;
	//! Create a copy of this SelectNode
	unique_ptr<QueryNode> Copy() override;
	//! Serializes a SelectNode to a stand-alone binary blob
	void Serialize(Serializer &serializer) override;
	//! Deserializes a blob back into a SelectNode
	static unique_ptr<QueryNode> Deserialize(Deserializer &source);
};
}; // namespace duckdb




namespace duckdb {

//! SelectStatement is a typical SELECT clause
class SelectStatement : public SQLStatement {
public:
	SelectStatement() : SQLStatement(StatementType::SELECT) {
	}

	bool Equals(const SQLStatement *other) const;

	//! CTEs
	unordered_map<string, unique_ptr<QueryNode>> cte_map;
	//! The main query node
	unique_ptr<QueryNode> node;

	//! Create a copy of this SelectStatement
	unique_ptr<SelectStatement> Copy();
	//! Serializes a SelectStatement to a stand-alone binary blob
	void Serialize(Serializer &serializer);
	//! Deserializes a blob back into a SelectStatement, returns nullptr if
	//! deserialization is not possible
	static unique_ptr<SelectStatement> Deserialize(Deserializer &source);
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/expression.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {
//!  The Expression class represents a bound Expression with a return type
class Expression : public BaseExpression {
public:
	Expression(ExpressionType type, ExpressionClass expression_class, TypeId return_type);

	//! The return type of the expression
	TypeId return_type;

public:
	bool IsAggregate() const override;
	bool IsWindow() const override;
	bool HasSubquery() const override;
	bool IsScalar() const override;
	bool HasParameter() const override;
	virtual bool IsFoldable() const;

	hash_t Hash() const override;

	static bool Equals(Expression *left, Expression *right) {
		return BaseExpression::Equals((BaseExpression *)left, (BaseExpression *)right);
	}
	//! Create a copy of this expression
	virtual unique_ptr<Expression> Copy() = 0;

protected:
	//! Copy base Expression properties from another expression to this one,
	//! used in Copy method
	void CopyProperties(Expression &other) {
		type = other.type;
		expression_class = other.expression_class;
		alias = other.alias;
		return_type = other.return_type;
	}
};

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/logical_operator.hpp
//
//
//===----------------------------------------------------------------------===//





//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/enums/logical_operator_type.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//===--------------------------------------------------------------------===//
// Logical Operator Types
//===--------------------------------------------------------------------===//
enum class LogicalOperatorType : uint8_t {
	INVALID,
	PROJECTION,
	FILTER,
	AGGREGATE_AND_GROUP_BY,
	WINDOW,
	UNNEST,
	LIMIT,
	ORDER_BY,
	TOP_N,
	COPY_FROM_FILE,
	COPY_TO_FILE,
	DISTINCT,
	INDEX_SCAN,
	// -----------------------------
	// Data sources
	// -----------------------------
	GET,
	CHUNK_GET,
	DELIM_GET,
	EXPRESSION_GET,
	TABLE_FUNCTION,
	EMPTY_RESULT,
	CTE_REF,
	// -----------------------------
	// Joins
	// -----------------------------
	JOIN,
	DELIM_JOIN,
	COMPARISON_JOIN,
	ANY_JOIN,
	CROSS_PRODUCT,
	// -----------------------------
	// SetOps
	// -----------------------------
	UNION,
	EXCEPT,
	INTERSECT,
	RECURSIVE_CTE,

	// -----------------------------
	// Updates
	// -----------------------------
	INSERT,
	DELETE,
	UPDATE,

	// -----------------------------
	// Schema
	// -----------------------------
	ALTER,
	CREATE_TABLE,
	CREATE_INDEX,
	CREATE_SEQUENCE,
	CREATE_VIEW,
	CREATE_SCHEMA,
	DROP,
	PRAGMA,
	TRANSACTION,

	// -----------------------------
	// Explain
	// -----------------------------
	EXPLAIN,

	// -----------------------------
	// Helpers
	// -----------------------------
	PRUNE_COLUMNS,
	PREPARE,
	EXECUTE,
	VACUUM
};

string LogicalOperatorToString(LogicalOperatorType type);

} // namespace duckdb


//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/logical_operator_visitor.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/bound_tokens.hpp
//
//
//===----------------------------------------------------------------------===//



namespace duckdb {

//===--------------------------------------------------------------------===//
// Statements
//===--------------------------------------------------------------------===//
class BoundSQLStatement;

class BoundCopyStatement;
class BoundCreateStatement;
class BoundDeleteStatement;
class BoundExecuteStatement;
class BoundExplainStatement;
class BoundInsertStatement;
class BoundSelectStatement;
class BoundUpdateStatement;
class BoundSimpleStatement;

//===--------------------------------------------------------------------===//
// Query Node
//===--------------------------------------------------------------------===//
class BoundQueryNode;
class BoundSelectNode;
class BoundSetOperationNode;
class BoundRecursiveCTENode;

//===--------------------------------------------------------------------===//
// Expressions
//===--------------------------------------------------------------------===//
class Expression;

class BoundAggregateExpression;
class BoundBetweenExpression;
class BoundCaseExpression;
class BoundCastExpression;
class BoundColumnRefExpression;
class BoundComparisonExpression;
class BoundConjunctionExpression;
class BoundConstantExpression;
class BoundDefaultExpression;
class BoundFunctionExpression;
class BoundOperatorExpression;
class BoundParameterExpression;
class BoundReferenceExpression;
class BoundSubqueryExpression;
class BoundUnnestExpression;
class BoundWindowExpression;
class CommonSubExpression;

//===--------------------------------------------------------------------===//
// TableRefs
//===--------------------------------------------------------------------===//
class BoundTableRef;

class BoundBaseTableRef;
class BoundCrossProductRef;
class BoundJoinRef;
class BoundSubqueryRef;
class BoundTableFunction;
class BoundEmptyTableRef;
class BoundExpressionListRef;
class BoundCTERef;

} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/logical_tokens.hpp
//
//
//===----------------------------------------------------------------------===//



namespace duckdb {

class LogicalOperator;

class LogicalAggregate;
class LogicalAnyJoin;
class LogicalChunkGet;
class LogicalComparisonJoin;
class LogicalCopyFromFile;
class LogicalCopyToFile;
class LogicalCreate;
class LogicalCreateTable;
class LogicalCreateIndex;
class LogicalCreateTable;
class LogicalCrossProduct;
class LogicalCTERef;
class LogicalDelete;
class LogicalDelimGet;
class LogicalDelimJoin;
class LogicalDistinct;
class LogicalEmptyResult;
class LogicalExecute;
class LogicalExplain;
class LogicalExpressionGet;
class LogicalFilter;
class LogicalGet;
class LogicalIndexScan;
class LogicalInsert;
class LogicalJoin;
class LogicalLimit;
class LogicalOrder;
class LogicalPrepare;
class LogicalProjection;
class LogicalPruneColumns;
class LogicalRecursiveCTE;
class LogicalSetOperation;
class LogicalSimple;
class LogicalTableFunction;
class LogicalTopN;
class LogicalUnnest;
class LogicalUpdate;
class LogicalWindow;

} // namespace duckdb


namespace duckdb {
//! The LogicalOperatorVisitor is an abstract base class that implements the
//! Visitor pattern on LogicalOperator.
class LogicalOperatorVisitor {
public:
	virtual ~LogicalOperatorVisitor(){};

	virtual void VisitOperator(LogicalOperator &op);
	virtual void VisitExpression(unique_ptr<Expression> *expression);

protected:
	//! Automatically calls the Visit method for LogicalOperator children of the current operator. Can be overloaded to
	//! change this behavior.
	void VisitOperatorChildren(LogicalOperator &op);
	//! Automatically calls the Visit method for Expression children of the current operator. Can be overloaded to
	//! change this behavior.
	void VisitOperatorExpressions(LogicalOperator &op);

	// The VisitExpressionChildren method is called at the end of every call to VisitExpression to recursively visit all
	// expressions in an expression tree. It can be overloaded to prevent automatically visiting the entire tree.
	virtual void VisitExpressionChildren(Expression &expression);

	virtual unique_ptr<Expression> VisitReplace(BoundAggregateExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundBetweenExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundCaseExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundCastExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundColumnRefExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundComparisonExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundConjunctionExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundConstantExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundDefaultExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundFunctionExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundOperatorExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundReferenceExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundSubqueryExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundParameterExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundWindowExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(BoundUnnestExpression &expr, unique_ptr<Expression> *expr_ptr);
	virtual unique_ptr<Expression> VisitReplace(CommonSubExpression &expr, unique_ptr<Expression> *expr_ptr);
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/column_binding.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

struct ColumnBinding {
	idx_t table_index;
	idx_t column_index;

	ColumnBinding() : table_index(INVALID_INDEX), column_index(INVALID_INDEX) {
	}
	ColumnBinding(idx_t table, idx_t column) : table_index(table), column_index(column) {
	}

	bool operator==(const ColumnBinding &rhs) const {
		return table_index == rhs.table_index && column_index == rhs.column_index;
	}
};

} // namespace duckdb


#include <functional>

namespace duckdb {

//! LogicalOperator is the base class of the logical operators present in the
//! logical query tree
class LogicalOperator {
public:
	LogicalOperator(LogicalOperatorType type) : type(type) {
	}
	LogicalOperator(LogicalOperatorType type, vector<unique_ptr<Expression>> expressions)
	    : type(type), expressions(move(expressions)) {
	}
	virtual ~LogicalOperator() {
	}

	//! The type of the logical operator
	LogicalOperatorType type;
	//! The set of children of the operator
	vector<unique_ptr<LogicalOperator>> children;
	//! The set of expressions contained within the operator, if any
	vector<unique_ptr<Expression>> expressions;
	//! The types returned by this logical operator. Set by calling LogicalOperator::ResolveTypes.
	vector<TypeId> types;

public:
	virtual vector<ColumnBinding> GetColumnBindings() {
		return {};
	}
	static vector<ColumnBinding> GenerateColumnBindings(idx_t table_idx, idx_t column_count);
	static vector<TypeId> MapTypes(vector<TypeId> types, vector<idx_t> projection_map);
	static vector<ColumnBinding> MapBindings(vector<ColumnBinding> types, vector<idx_t> projection_map);

	//! Resolve the types of the logical operator and its children
	void ResolveOperatorTypes();

	virtual string ParamsToString() const;
	virtual string ToString(idx_t depth = 0) const;
	void Print();

	void AddChild(unique_ptr<LogicalOperator> child) {
		children.push_back(move(child));
	}

	virtual idx_t EstimateCardinality() {
		// simple estimator, just take the max of the children
		idx_t max_cardinality = 0;
		for (auto &child : children) {
			max_cardinality = std::max(child->EstimateCardinality(), max_cardinality);
		}
		return max_cardinality;
	}

protected:
	//! Resolve types for this specific operator
	virtual void ResolveTypes() = 0;
};
} // namespace duckdb


namespace duckdb {
class ClientContext;
class ExpressionExecutor;
class PhysicalOperator;

//! The current state/context of the operator. The PhysicalOperatorState is
//! updated using the GetChunk function, and allows the caller to repeatedly
//! call the GetChunk function and get new batches of data everytime until the
//! data source is exhausted.
class PhysicalOperatorState {
public:
	PhysicalOperatorState(PhysicalOperator *child);
	virtual ~PhysicalOperatorState() = default;

	//! Flag indicating whether or not the operator is finished [note: not all
	//! operators use this flag]
	bool finished;
	//! DataChunk that stores data from the child of this operator
	DataChunk child_chunk;
	//! State of the child of this operator
	unique_ptr<PhysicalOperatorState> child_state;
};

//! PhysicalOperator is the base class of the physical operators present in the
//! execution plan
/*!
    The execution model is a pull-based execution model. GetChunk is called on
   the root node, which causes the root node to be executed, and presumably call
   GetChunk again on its child nodes. Every node in the operator chain has a
   state that is updated as GetChunk is called: PhysicalOperatorState (different
   operators subclass this state and add different properties).
*/
class PhysicalOperator {
public:
	PhysicalOperator(PhysicalOperatorType type, vector<TypeId> types) : type(type), types(types) {
	}
	virtual ~PhysicalOperator() {
	}

	//! The physical operator type
	PhysicalOperatorType type;
	//! The set of children of the operator
	vector<unique_ptr<PhysicalOperator>> children;
	//! The types returned by this physical operator
	vector<TypeId> types;

public:
	string ToString(idx_t depth = 0) const;
	void Print();

	//! Return a vector of the types that will be returned by this operator
	vector<TypeId> &GetTypes() {
		return types;
	}
	//! Initialize a given chunk to the types that will be returned by this
	//! operator, this will prepare chunk for a call to GetChunk. This method
	//! only has to be called once for any amount of calls to GetChunk.
	virtual void InitializeChunk(DataChunk &chunk) {
		auto &types = GetTypes();
		chunk.Initialize(types);
	}
	//! Retrieves a chunk from this operator and stores it in the chunk
	//! variable.
	virtual void GetChunkInternal(ClientContext &context, DataChunk &chunk, PhysicalOperatorState *state) = 0;

	void GetChunk(ClientContext &context, DataChunk &chunk, PhysicalOperatorState *state);

	//! Create a new empty instance of the operator state
	virtual unique_ptr<PhysicalOperatorState> GetOperatorState() {
		return make_unique<PhysicalOperatorState>(children.size() == 0 ? nullptr : children[0].get());
	}

	virtual string ExtraRenderInformation() const {
		return "";
	}
};
} // namespace duckdb



namespace duckdb {
class DuckDB;

class ExecutionContext {
public:
	unique_ptr<PhysicalOperator> physical_plan;
	unique_ptr<PhysicalOperatorState> physical_state;

public:
	void Reset() {
		physical_plan = nullptr;
		physical_state = nullptr;
	}
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/main/query_profiler.hpp
//
//
//===----------------------------------------------------------------------===//




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/profiler.hpp
//
//
//===----------------------------------------------------------------------===//





#include <chrono>

namespace duckdb {

//! The profiler can be used to measure elapsed time
class Profiler {
public:
	//! Starts the timer
	void Start() {
		finished = false;
		start = Tick();
	}
	//! Finishes timing
	void End() {
		end = Tick();
		finished = true;
	}

	//! Returns the elapsed time in seconds. If End() has been called, returns
	//! the total elapsed time. Otherwise returns how far along the timer is
	//! right now.
	double Elapsed() const {
		auto _end = finished ? end : Tick();
		return std::chrono::duration_cast<std::chrono::duration<double>>(_end - start).count();
	}

private:
	std::chrono::time_point<std::chrono::system_clock> Tick() const {
		return std::chrono::system_clock::now();
	}
	std::chrono::time_point<std::chrono::system_clock> start;
	std::chrono::time_point<std::chrono::system_clock> end;
	bool finished = false;
};
} // namespace duckdb

//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/string_util.hpp
//
//
//===----------------------------------------------------------------------===//




#include <stdarg.h> // for va_list

namespace duckdb {
/**
 * String Utility Functions
 * Note that these are not the most efficient implementations (i.e., they copy
 * memory) and therefore they should only be used for debug messages and other
 * such things.
 */
class StringUtil {
public:
	//! Returns true if the needle string exists in the haystack
	static bool Contains(const string &haystack, const string &needle);

	//! Returns true if the target string starts with the given prefix
	static bool StartsWith(const string &str, const string &prefix);

	//! Returns true if the target string <b>ends</b> with the given suffix.
	static bool EndsWith(const string &str, const string &suffix);

	//! Repeat a string multiple times
	static string Repeat(const string &str, const idx_t n);

	//! Split the input string based on newline char
	static vector<string> Split(const string &str, char delimiter);

	//! Join multiple strings into one string. Components are concatenated by the given separator
	static string Join(const vector<string> &input, const string &separator);

	//! Join multiple items of container with given size, transformed to string
	//! using function, into one string using the given separator
	template <typename C, typename S, typename Func>
	static string Join(const C &input, S count, const string &separator, Func f) {
		// The result
		std::string result;

		// If the input isn't empty, append the first element. We do this so we
		// don't need to introduce an if into the loop.
		if (count > 0) {
			result += f(input[0]);
		}

		// Append the remaining input components, after the first
		for (size_t i = 1; i < count; i++) {
			result += separator + f(input[i]);
		}

		return result;
	}

	//! Append the prefix to the beginning of each line in str
	static string Prefix(const string &str, const string &prefix);

	//! Return a string that formats the give number of bytes
	static string FormatSize(idx_t bytes);

	//! Convert a string to uppercase
	static string Upper(const string &str);

	//! Convert a string to lowercase
	static string Lower(const string &str);

	//! Format a string using printf semantics
	static string Format(const string fmt_str, ...);
	static string VFormat(const string fmt_str, va_list ap);

	//! Split the input string into a vector of strings based on the split string
	static vector<string> Split(const string &input, const string &split);

	//! Remove the whitespace char in the left end of the string
	static void LTrim(string &str);
	//! Remove the whitespace char in the right end of the string
	static void RTrim(string &str);
	//! Remove the whitespace char in the left and right end of the string
	static void Trim(string &str);

	static string Replace(string source, const string &from, const string &to);
};
} // namespace duckdb





#include <stack>
#include <unordered_map>

namespace duckdb {
class PhysicalOperator;
class SQLStatement;

//! The QueryProfiler can be used to measure timings of queries
class QueryProfiler {
public:
	struct TimingInformation {
		double time = 0;
		idx_t elements = 0;

		TimingInformation() : time(0), elements(0) {
		}
	};
	struct TreeNode {
		string name;
		string extra_info;
		vector<string> split_extra_info;
		TimingInformation info;
		vector<unique_ptr<TreeNode>> children;
		idx_t depth = 0;
	};

private:
	static idx_t GetDepth(QueryProfiler::TreeNode &node);
	unique_ptr<TreeNode> CreateTree(PhysicalOperator *root, idx_t depth = 0);

	static idx_t RenderTreeRecursive(TreeNode &node, vector<string> &render, vector<idx_t> &render_heights,
	                                 idx_t base_render_x = 0, idx_t start_depth = 0, idx_t depth = 0);
	static string RenderTree(TreeNode &node);

public:
	QueryProfiler() : automatic_print_format(ProfilerPrintFormat::NONE), enabled(false), running(false) {
	}

	void Enable() {
		enabled = true;
	}

	void Disable() {
		enabled = false;
	}

	bool IsEnabled() {
		return enabled;
	}

	void StartQuery(string query, SQLStatement &statement);
	void EndQuery();

	void StartPhase(string phase);
	void EndPhase();

	void StartOperator(PhysicalOperator *phys_op);
	void EndOperator(DataChunk &chunk);

	string ToString() const;
	void Print();

	string ToJSON() const;
	void WriteToFile(const char *path, string &info) const;

	//! The format to automatically print query profiling information in (default: disabled)
	ProfilerPrintFormat automatic_print_format;
	//! The file to save query profiling information to, instead of printing it to the console (empty = print to
	//! console)
	string save_location;

private:
	//! Whether or not query profiling is enabled
	bool enabled;
	//! Whether or not the query profiler is running
	bool running;

	//! The root of the query tree
	unique_ptr<TreeNode> root;
	//! The query string
	string query;

	//! The timer used to time the execution time of the entire query
	Profiler main_query;
	//! The timer used to time the execution time of the individual Physical Operators
	Profiler op;
	//! A map of a Physical Operator pointer to a tree node
	unordered_map<PhysicalOperator *, TreeNode *> tree_map;
	//! The stack of Physical Operators that are currently active
	std::stack<PhysicalOperator *> execution_stack;

	//! The timer used to time the individual phases of the planning process
	Profiler phase_profiler;
	//! A mapping of the phase names to the timings
	using PhaseTimingStorage = unordered_map<string, double>;
	PhaseTimingStorage phase_timings;
	using PhaseTimingItem = PhaseTimingStorage::value_type;
	//! The stack of currently active phases
	vector<string> phase_stack;

private:
	vector<PhaseTimingItem> GetOrderedPhaseTimings() const;
};
} // namespace duckdb




//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/transaction/transaction_context.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

class Transaction;
class TransactionManager;

//! The transaction context keeps track of all the information relating to the
//! current transaction
class TransactionContext {
public:
	TransactionContext(TransactionManager &transaction_manager)
	    : transaction_manager(transaction_manager), auto_commit(true), is_invalidated(false),
	      current_transaction(nullptr) {
	}
	~TransactionContext();

	Transaction &ActiveTransaction() {
		assert(current_transaction);
		return *current_transaction;
	}

	bool HasActiveTransaction() {
		return !!current_transaction;
	}

	void RecordQuery(string query);
	void BeginTransaction();
	void Commit();
	void Rollback();

	void SetAutoCommit(bool value) {
		auto_commit = value;
	}
	bool IsAutoCommit() {
		return auto_commit;
	}

	void Invalidate() {
		is_invalidated = true;
	}

private:
	TransactionManager &transaction_manager;
	bool auto_commit;
	bool is_invalidated;

	Transaction *current_transaction;

	TransactionContext(const TransactionContext &) = delete;
};

} // namespace duckdb


#include <random>

namespace duckdb {
class Appender;
class Catalog;
class DuckDB;
class PreparedStatementData;

//! The ClientContext holds information relevant to the current client session
//! during execution
class ClientContext {
public:
	ClientContext(DuckDB &database);

	//! Query profiler
	QueryProfiler profiler;
	//! The database that this client is connected to
	DuckDB &db;
	//! Data for the currently running transaction
	TransactionContext transaction;
	//! Whether or not the query is interrupted
	bool interrupted;
	//! Whether or not the ClientContext has been invalidated because the underlying database is destroyed
	bool is_invalidated = false;
	//! Lock on using the ClientContext in parallel
	std::mutex context_lock;

	ExecutionContext execution_context;

	Catalog &catalog;
	unique_ptr<SchemaCatalogEntry> temporary_objects;
	unique_ptr<CatalogSet> prepared_statements;

	// Whether or not aggressive query verification is enabled
	bool query_verification_enabled = false;
	//! Enable the running of optimizers
	bool enable_optimizer = true;

	//! The random generator used by random(). Its seed value can be set by setseed().
	std::mt19937 random_engine;

public:
	Transaction &ActiveTransaction() {
		return transaction.ActiveTransaction();
	}

	//! Interrupt execution of a query
	void Interrupt();
	//! Enable query profiling
	void EnableProfiling();
	//! Disable query profiling
	void DisableProfiling();

	//! Issue a query, returning a QueryResult. The QueryResult can be either a StreamQueryResult or a
	//! MaterializedQueryResult. The StreamQueryResult will only be returned in the case of a successful SELECT
	//! statement.
	unique_ptr<QueryResult> Query(string query, bool allow_stream_result);
	//! Fetch a query from the current result set (if any)
	unique_ptr<DataChunk> Fetch();
	//! Cleanup the result set (if any).
	void Cleanup();
	//! Invalidate the client context. The current query will be interrupted and the client context will be invalidated,
	//! making it impossible for future queries to run.
	void Invalidate();

	//! Get the table info of a specific table, or nullptr if it cannot be found
	unique_ptr<TableDescription> TableInfo(string schema_name, string table_name);
	//! Appends a DataChunk to the specified table. Returns whether or not the append was successful.
	void Append(TableDescription &description, DataChunk &chunk);

	//! Prepare a query
	unique_ptr<PreparedStatement> Prepare(string query);
	//! Execute a prepared statement with the given name and set of parameters
	unique_ptr<QueryResult> Execute(string name, vector<Value> &values, bool allow_stream_result = true,
	                                string query = string());
	//! Removes a prepared statement from the set of prepared statements in the client context
	void RemovePreparedStatement(PreparedStatement *statement);

	void RegisterAppender(Appender *appender);
	void RemoveAppender(Appender *appender);

private:
	//! Perform aggressive query verification of a SELECT statement. Only called when query_verification_enabled is
	//! true.
	string VerifyQuery(string query, unique_ptr<SQLStatement> statement);

	void InitialCleanup();
	//! Internal clean up, does not lock. Caller must hold the context_lock.
	void CleanupInternal();
	string FinalizeQuery(bool success);
	//! Internal fetch, does not lock. Caller must hold the context_lock.
	unique_ptr<DataChunk> FetchInternal();
	//! Internally execute a set of SQL statement. Caller must hold the context_lock.
	unique_ptr<QueryResult> RunStatements(const string &query, vector<unique_ptr<SQLStatement>> &statements,
	                                      bool allow_stream_result);
	//! Internally prepare and execute a prepared SQL statement. Caller must hold the context_lock.
	unique_ptr<QueryResult> RunStatement(const string &query, unique_ptr<SQLStatement> statement,
	                                     bool allow_stream_result);

	//! Internally prepare a SQL statement. Caller must hold the context_lock.
	unique_ptr<PreparedStatementData> CreatePreparedStatement(const string &query, unique_ptr<SQLStatement> statement);
	//! Internally execute a prepared SQL statement. Caller must hold the context_lock.
	unique_ptr<QueryResult> ExecutePreparedStatement(const string &query, PreparedStatementData &statement,
	                                                 vector<Value> bound_values, bool allow_stream_result);
	//! Call CreatePreparedStatement() and ExecutePreparedStatement() without any bound values
	unique_ptr<QueryResult> RunStatementInternal(const string &query, unique_ptr<SQLStatement> statement,
	                                             bool allow_stream_result);

private:
	idx_t prepare_count = 0;
	//! The currently opened StreamQueryResult (if any)
	StreamQueryResult *open_result = nullptr;
	//! Prepared statement objects that were created using the ClientContext::Prepare method
	unordered_set<PreparedStatement *> prepared_statement_objects;
	//! Appenders that were attached to this client context
	unordered_set<Appender *> appenders;
};
} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/function/function.hpp
//
//
//===----------------------------------------------------------------------===//







namespace duckdb {
class CatalogEntry;
class Catalog;
class ClientContext;
class Expression;
class ExpressionExecutor;
class Transaction;

class AggregateFunction;
class AggregateFunctionSet;
class ScalarFunctionSet;
class ScalarFunction;
class TableFunction;

struct FunctionData {
	virtual ~FunctionData() {
	}

	virtual unique_ptr<FunctionData> Copy() = 0;
};

struct TableFunctionData : public FunctionData {
	unique_ptr<FunctionData> Copy() override {
		throw NotImplementedException("Copy not required for table-producing function");
	}
};

//! Function is the base class used for any type of function (scalar, aggregate or simple function)
class Function {
public:
	Function(string name) : name(name) {
	}
	virtual ~Function() {
	}

	//! The name of the function
	string name;

public:
	//! Returns the formatted string name(arg1, arg2, ...)
	static string CallToString(string name, vector<SQLType> arguments);
	//! Returns the formatted string name(arg1, arg2..) -> return_type
	static string CallToString(string name, vector<SQLType> arguments, SQLType return_type);

	//! Bind a scalar function from the set of functions and input arguments. Returns the index of the chosen function,
	//! or throws an exception if none could be found.
	static idx_t BindFunction(string name, vector<ScalarFunction> &functions, vector<SQLType> &arguments);
	//! Bind an aggregate function from the set of functions and input arguments. Returns the index of the chosen
	//! function, or throws an exception if none could be found.
	static idx_t BindFunction(string name, vector<AggregateFunction> &functions, vector<SQLType> &arguments);
};

class SimpleFunction : public Function {
public:
	SimpleFunction(string name, vector<SQLType> arguments, SQLType return_type, bool has_side_effects)
	    : Function(name), arguments(move(arguments)), return_type(return_type), varargs(SQLTypeId::INVALID),
	      has_side_effects(has_side_effects) {
	}
	virtual ~SimpleFunction() {
	}

	//! The set of arguments of the function
	vector<SQLType> arguments;
	//! Return type of the function
	SQLType return_type;
	//! The type of varargs to support, or SQLTypeId::INVALID if the function does not accept variable length arguments
	SQLType varargs;
	//! Whether or not the function has side effects (e.g. sequence increments, random() functions, NOW()). Functions
	//! with side-effects cannot be constant-folded.
	bool has_side_effects;

public:
	//! Cast a set of expressions to the arguments of this function
	void CastToFunctionArguments(vector<unique_ptr<Expression>> &children, vector<SQLType> &types);

	string ToString() {
		return Function::CallToString(name, arguments, return_type);
	}

	bool HasVarArgs() {
		return varargs.id != SQLTypeId::INVALID;
	}
};

class BuiltinFunctions {
public:
	BuiltinFunctions(ClientContext &transaction, Catalog &catalog);

	//! Initialize a catalog with all built-in functions
	void Initialize();

public:
	void AddFunction(AggregateFunctionSet set);
	void AddFunction(AggregateFunction function);
	void AddFunction(ScalarFunctionSet set);
	void AddFunction(ScalarFunction function);
	void AddFunction(TableFunction function);

private:
	ClientContext &context;
	Catalog &catalog;

private:
	template <class T> void Register() {
		T::RegisterFunction(*this);
	}

	// table-producing functions
	void RegisterSQLiteFunctions();
	void RegisterReadFunctions();

	// aggregates
	void RegisterAlgebraicAggregates();
	void RegisterDistributiveAggregates();
	void RegisterNestedAggregates();

	// scalar functions
	void RegisterDateFunctions();
	void RegisterMathFunctions();
	void RegisterOperators();
	void RegisterStringFunctions();
	void RegisterNestedFunctions();
	void RegisterSequenceFunctions();
	void RegisterTrigonometricsFunctions();
};

} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/function/table_function.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

//! Function used for determining the return type of a table producing function
typedef unique_ptr<FunctionData> (*table_function_bind_t)(ClientContext &context, vector<Value> inputs,
                                                          vector<SQLType> &return_types, vector<string> &names);
//! Type used for table-returning function
typedef void (*table_function_t)(ClientContext &context, vector<Value> &input, DataChunk &output,
                                 FunctionData *dataptr);
//! Type used for final (cleanup) function
typedef void (*table_function_final_t)(ClientContext &context, FunctionData *dataptr);

class TableFunction : public Function {
public:
	TableFunction(string name, vector<SQLType> arguments, table_function_bind_t bind, table_function_t function,
	              table_function_final_t final)
	    : Function(name), arguments(move(arguments)), bind(bind), function(function), final(final) {
	}

	//! Input arguments
	vector<SQLType> arguments;
	//! The bind function
	table_function_bind_t bind;
	//! The function pointer
	table_function_t function;
	//! Final function pointer
	table_function_final_t final;
};

} // namespace duckdb
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_table_function_info.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_info.hpp
//
//
//===----------------------------------------------------------------------===//



//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/parse_info.hpp
//
//
//===----------------------------------------------------------------------===//





namespace duckdb {

struct ParseInfo {
	virtual ~ParseInfo() {
	}
};

} // namespace duckdb



namespace duckdb {

enum class OnCreateConflict : uint8_t {
	// Standard: throw error
	ERROR,
	// CREATE IF NOT EXISTS, silently do nothing on conflict
	IGNORE,
	// CREATE OR REPLACE
	REPLACE
};

struct CreateInfo : public ParseInfo {
	CreateInfo(CatalogType type, string schema = DEFAULT_SCHEMA)
	    : type(type), schema(schema), on_conflict(OnCreateConflict::ERROR), temporary(false) {
	}
	virtual ~CreateInfo() {
	}

	//! The to-be-created catalog type
	CatalogType type;
	//! The schema name of the entry
	string schema;
	//! What to do on create conflict
	OnCreateConflict on_conflict;
	//! Whether or not the entry is temporary
	bool temporary;
};

} // namespace duckdb



namespace duckdb {

struct CreateTableFunctionInfo : public CreateInfo {
	CreateTableFunctionInfo(TableFunction function) : CreateInfo(CatalogType::TABLE_FUNCTION), function(function) {
		this->name = function.name;
	}

	//! Function name
	string name;
	//! The table function
	TableFunction function;
};

} // namespace duckdb
