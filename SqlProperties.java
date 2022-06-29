package freshdesk;
import java.util.ResourceBundle;


public class SqlProperties {

	private static SqlProperties sqlProperties = null;
	private static ResourceBundle sqlResource = null;
	
	private SqlProperties() {
		sqlResource = ResourceBundle.getBundle("sql");
		
	}
	
	public static SqlProperties getInstance() {
		return sqlProperties == null? sqlProperties = new SqlProperties() : sqlProperties;
	}
	
	public String getValue(String key) {
		return sqlResource.getString(key);
	}
}
