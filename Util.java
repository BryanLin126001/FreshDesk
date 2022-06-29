package freshdesk;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Util {
	
	public static String getDynamicId() {
		String pattern = "yyyyMMddkkmmssSSS";
		LocalDateTime datetime = LocalDateTime.now();
		datetime.format(DateTimeFormatter.ofPattern(pattern)).toString();
		return datetime.format(DateTimeFormatter.ofPattern(pattern)).toString();
	}

}
