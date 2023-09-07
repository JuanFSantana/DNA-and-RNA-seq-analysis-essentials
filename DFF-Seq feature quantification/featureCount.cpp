#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <set>
#include <nlohmann/json.hpp>
#include <fstream> 

struct IntervalSize {
    std::string geneName;
    std::string featureName;
    int startPosition;
    int endPosition;
    int startSize;
    int endSize;
    int count = 0;  // to store the count of sizes falling in this interval
    double normCount = 0.0;  // to store the count of sizes falling in this interval normalized by correction factor
};

enum class ObjectType {
    Centers, // the center of the read
    FullOverlap, // the whole reads should fall within the region
    PartialOverlap // at least 1 bp of the read falls within the region
};

ObjectType convertStrObject(const std::string& overlapType);
void makeIntervalStruct(const nlohmann::json& data, std::vector<IntervalSize>& intervals, std::ifstream& readsBed);
void countFeatures(std::vector<IntervalSize>& intervals, std::ifstream& readsBed, const size_t numOfFeatures, ObjectType readAnalysisType, double correctionFactor);
void outputIntervals(const std::vector<IntervalSize>& intervals, const nlohmann::json& data, const std::string& outputName);

int main(int argc, char* argv[]) {
    // make sure that 6 arguments are passed
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " <path_to_reads_bed_file> <json_data> <output_name> <type_of_overlap (centers, full, partial)> <correction_factor>" << std::endl << std::endl;
        exit(EXIT_FAILURE);
        return 1;
    }

    // check for valid type_of_overlap option and establish type of analysis; declaring bedFilePath to be opened, jsonData to be parsed 
    std::string readsBedFilePath  = argv[1];
    std::string jsonData = argv[2];
    std::string outputName = argv[3];
    std::string overlapType(argv[4]);
    double correctionFactor = std::stod(argv[5]); // convert string to double

    ObjectType readAnalysisType;
    if (overlapType != "centers" && overlapType != "full" && overlapType != "partial") {
        std::cerr << "Invalid type_of_overlap option. Please choose from 'centers', 'full', or 'partial'." << std::endl;
        exit(EXIT_FAILURE);
        return 1;
    }else{
        readAnalysisType = convertStrObject(overlapType);
    }
    // parse the JSON data
    nlohmann::json data = nlohmann::json::parse(jsonData);
    size_t numOfFeatures = data.size();
    // open bed file
    std::ifstream readsBed(readsBedFilePath);      
    if (!readsBed) {
            std::cerr << "Error: could not open file " << readsBedFilePath << std::endl;
            exit(EXIT_FAILURE);
        }
    // create vector of Interval objects
    std::vector<IntervalSize> intervals;
    // initialize interval objects with data from JSON
    makeIntervalStruct(data, intervals, readsBed);
    // count the reads belonging to each feature for each gene
    countFeatures(intervals, readsBed, numOfFeatures, readAnalysisType, correctionFactor);
    // output results
    outputIntervals(intervals, data, outputName);

    return 0;
}

ObjectType convertStrObject(const std::string& overlapType){
    if (overlapType == "centers") return ObjectType::Centers;
    if (overlapType == "full") return ObjectType::FullOverlap;
    if (overlapType == "partial") return ObjectType::PartialOverlap;

    std::cerr << "Error: Invalid overlapType provided: " << overlapType << std::endl;
    exit(EXIT_FAILURE);
    }

void makeIntervalStruct(const nlohmann::json& data, std::vector<IntervalSize>& intervals, std::ifstream& readsBed) {
    std::string col0, col1, col2, genes;
    std::set<std::string> uniqueGeneNameChecker;
    std::vector<std::string> orderedUniqueGeneNames;

    while (readsBed >> col0 >> col1 >> col2 >> genes) {
        // ignore the rest of the columns
        readsBed.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (uniqueGeneNameChecker.insert(genes).second) {
            // .second of the pair returned by .insert() is true if the insertion took place, i.e., the item was unique
            orderedUniqueGeneNames.push_back(genes);
        }
    }
        

    // make a struct for each gene with the feature information
    for (const auto& uniqueGene : orderedUniqueGeneNames) {
        for (const auto& [feature, distancesize] : data.items()){
            IntervalSize interval;  
            interval.geneName = uniqueGene;
            interval.featureName = feature;
            interval.startPosition = distancesize[0][0];
            interval.endPosition = distancesize[0][1];
            interval.startSize = distancesize[1][0];
            interval.endSize = distancesize[1][1];
            intervals.push_back(interval);  
        }
    }
}


void countFeatures(std::vector<IntervalSize>& intervals, std::ifstream& readsBed, const size_t numOfFeatures, ObjectType readAnalysisType, double correctionFactor) {
    // declare variables to store bed file information from bedtools output
    std::string regionChr; // col1
    int regionStart; // col2
    int regionEnd; // col3
    std::string regionGene; // col4
    std::string additionalInfo1; // col5
    std::string regionStrand; // col6      
    std::string readsChr; // col7
    int readsStart; // col8
    int readsEnd; // col9
    std::string readsID; // col 10 
    int readsQual; // col 11
    std::string readsStrand; // col12 

    size_t currentIntervalIndex1 = 0;
    size_t currentIntervalIndex2 = 0;
    std::string old_gene = "";

    readsBed.clear(); // clear any flags, especially EOF
    readsBed.seekg(0, std::ios::beg); // reset file pointer to the beginning
    while (readsBed >> regionChr >> regionStart >> regionEnd >> regionGene >> additionalInfo1 >> regionStrand >> readsChr >> readsStart >> readsEnd >> readsID >> readsQual >> readsStrand) {
        int readSize = (readsEnd - readsStart) + 1;
        std::string current_gene = regionGene;
        int readBasePositionStart;
        int readBasePositionEnd;
        int positionTSS = (regionStart + regionEnd) / 2;
        float readCenter;
        // calculate read position relative to TSS in the middle of the region
        if (regionStrand == "+"){
            readBasePositionStart = readsStart - positionTSS;
            readBasePositionEnd = readsEnd - positionTSS;

            // if centers
            if (readAnalysisType == ObjectType::Centers){
                readCenter = ((readsStart + readsEnd) / 2) - positionTSS;
            }
        }

        else if (regionStrand == "-"){
            readBasePositionStart = positionTSS - readsEnd;
            readBasePositionEnd = positionTSS - readsStart; 

            // if centers
            if (readAnalysisType == ObjectType::Centers){
                readCenter = positionTSS - ((readsStart + readsEnd) / 2);
            }
        }

        // if the postion is 0 or positive, add 1 to the position to reflect starting at +1
        if (readBasePositionStart >= 0){
            readBasePositionStart += 1;
        }
        if (readBasePositionEnd >= 0){
            readBasePositionEnd += 1;
        }

        if (current_gene != old_gene && currentIntervalIndex2 > 0){
            currentIntervalIndex1 += numOfFeatures;
        }

        // loop through all intervals to check if this read matches any of them
        for (int i = currentIntervalIndex1; i < intervals.size(); i++) {
            if (regionGene == intervals[i].geneName){
                // is the analysis centers, full read overlap or partial overlap of at leat 1 bp
                switch (readAnalysisType){
                    case ObjectType::FullOverlap:
                        if((readBasePositionStart >= intervals[i].startPosition && readBasePositionEnd <= intervals[i].endPosition) &&
                        (readSize >= intervals[i].startSize && readSize <= intervals[i].endSize)){
                            intervals[i].count++;
                            intervals[i].normCount += 1 * correctionFactor;
                        }
                        break;

                    case ObjectType::PartialOverlap:
                        if (((readBasePositionStart >= intervals[i].startPosition && readBasePositionStart <= intervals[i].endPosition) ||
                            (readBasePositionEnd >= intervals[i].startPosition && readBasePositionEnd <= intervals[i].endPosition)) &&
                            (readSize >= intervals[i].startSize && readSize <= intervals[i].endSize)) {
                                intervals[i].count++;
                                intervals[i].normCount += 1 * correctionFactor;
                        }
                        break;

                    case ObjectType::Centers:{
                        if((readCenter >= intervals[i].startPosition && readCenter <= intervals[i].endPosition) &&
                        (readSize >= intervals[i].startSize && readSize <= intervals[i].endSize)){
                            intervals[i].count++;
                            intervals[i].normCount += 1 * correctionFactor;
                        }
                        break;
                    }
                    default:
                        std::cerr << "Unexpected ObjectType encountered. Exiting program." << std::endl;
                        exit(EXIT_FAILURE);
                }

            }
            else{
                break;
            }

        old_gene = current_gene;

        }

        currentIntervalIndex2++;
    }
}


void outputIntervals(const std::vector<IntervalSize>& intervals, const nlohmann::json& data, const std::string& outputName) {
    std::ofstream outFile(outputName);
    if (!outFile) {
        std::cerr << "Error: Unable to open output file for writing." << std::endl;
        exit(EXIT_FAILURE);
        return;
    }

    // Write header
    std::string fileHeader = "Genes\t";
    for (auto& [key,value]: data.items()){
        fileHeader += key + "\t" + key + "-normalized\t";
    }
    //  remove the trailing tab
    if (!fileHeader.empty()) {
        fileHeader.pop_back();
    }
    // write out header
    outFile << fileHeader << "\n";

    // write data for each interval
    std::string old_gene = "";
    std::string line = "";
    size_t currentIntervalIndex1 = 0;
    for (const auto& interval : intervals) {
        std::string current_gene = interval.geneName;

        if (currentIntervalIndex1 == 0 || current_gene == old_gene){
            line += std::to_string(interval.count) + "\t" + std::to_string(interval.normCount) + "\t";
            currentIntervalIndex1++;
        }
        else{
            line = old_gene + "\t" + line;
            // remove last tab
            line.pop_back();
            // output with new line
            outFile << line << "\n";
            line = std::to_string(interval.count) + "\t" + std::to_string(interval.normCount) + "\t";
        }

        old_gene = current_gene;
    }

    if (!line.empty()) {
        line = old_gene + "\t" + line;
        line.pop_back();
        outFile << line << "\n";
    }

    outFile.close();
}

    

