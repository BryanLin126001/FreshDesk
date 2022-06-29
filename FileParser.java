package freshdesk;

import com.google.gson.*;
import freshdesk.vo.FreshdeskActivitiesVO;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;



public class FileParser {
	
	private File f = null;
	private static final Logger logger = LogManager.getLogger(FileParser.class);
	
	public FileParser(String jsonFileName) {
		this.f = new File(jsonFileName);
	}
	
	public BufferedReader getJsonFileReader() {
		
		BufferedReader reader = null; 
		try {
			reader = new BufferedReader(new FileReader(this.f));
		}
		catch(Exception e) {
			logger.error("getJsonFileReader error, msg: " + e.getMessage());
		}
		return reader;
	}
	
	public FreshdeskActivitiesVO getFreshdeskActivitiesVOFromJsonFile(BufferedReader reader) {
		
		Gson gson = new GsonBuilder().create();
		FreshdeskActivitiesVO freshdeskActivitiesVO = gson.fromJson(reader, FreshdeskActivitiesVO.class);
		return freshdeskActivitiesVO;
	}
}
