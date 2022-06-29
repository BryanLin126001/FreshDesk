package freshdesk.vo;

public class ActivitiesDataVO {
	private String performed_at;
	private int ticket_id;
	private String performer_type;
	private int performer_id;
	private ActivityVO activity;
	
	public String getPerformed_at() {
		return performed_at;
	}
	public void setPerformed_at(String performed_at) {
		this.performed_at = performed_at;
	}
	public int getTicket_id() {
		return ticket_id;
	}
	public void setTicket_id(int ticket_id) {
		this.ticket_id = ticket_id;
	}
	public String getPerformer_type() {
		return performer_type;
	}
	public void setPerformer_type(String performer_type) {
		this.performer_type = performer_type;
	}
	public int getPerformer_id() {
		return performer_id;
	}
	public void setPerformer_id(int performer_id) {
		this.performer_id = performer_id;
	}
	public ActivityVO getActivity() {
		return activity;
	}
	public void setActivity(ActivityVO activity) {
		this.activity = activity;
	}
	
	

}
