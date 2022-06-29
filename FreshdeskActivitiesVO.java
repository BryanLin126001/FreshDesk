package freshdesk.vo;
import java.util.ArrayList;

public class FreshdeskActivitiesVO {
	private ActivitiesMetadataVO metadata;
	private ArrayList<ActivitiesDataVO> activities_data;
	
	public ActivitiesMetadataVO getMetadata() {
		return metadata;
	}
	public void setMetadata(ActivitiesMetadataVO metadata) {
		this.metadata = metadata;
	}
	public ArrayList<ActivitiesDataVO> getActivities_data() {
		return activities_data;
	}
	public void setActivities_data(ArrayList<ActivitiesDataVO> activities_data) {
		this.activities_data = activities_data;
	}

}
