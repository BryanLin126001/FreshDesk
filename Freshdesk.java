package freshdesk;

import java.io.BufferedReader;
import freshdesk.dao.FreshdeskDAO;
import freshdesk.vo.FreshdeskActivitiesVO;

public class Freshdesk {

	public static void showHelp() {
		String helpMsg = "Freshdesk is been used to parse JSON ticket file into database. \n"
				+ "where: \n"
				+ "-p: Indicate ticket JSON file to parse."
				+ "example: freshdesk.Freshdesk -p /home/userhome/activities.json";
		System.out.println(helpMsg);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		if (args[0].equals("-p")) {
			FileParser jsonParser = new FileParser(args[1]);
			BufferedReader jsonReader = jsonParser.getJsonFileReader();
			FreshdeskActivitiesVO freshdeskActivitiesVO =  jsonParser.getFreshdeskActivitiesVOFromJsonFile(jsonReader);
			FreshdeskDAO freshdeskDao = new FreshdeskDAO();
			freshdeskDao.addDataFromJsonFile(freshdeskActivitiesVO);
		}
		else if(args[0].equals("-h")) {
			Freshdesk.showHelp();
		}
		else {
			System.out.println("Use fresh.Fresh -h to get help.");
		}
	}
}
