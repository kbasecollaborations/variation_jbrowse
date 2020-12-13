/*
A KBase module: variation_jbrowse
This sample module contains one small method that filters contigs.
*/

module variation_jbrowse {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_variation_jbrowse(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
