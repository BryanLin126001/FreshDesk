package freshdesk.vo;

public class ActivityVO {
	private String shipping_address;
	private String shipment_date;
	private String category;
	private boolean contacted_customer;
	private String issue_type;
	private int source;
	private String status;
	private int priority;
	private String group;
	private int agent_id;
	private int requester;
	private String product;
	private ActivityNoteVO note;
	
	public String getShipping_address() {
		return shipping_address;
	}
	public void setShipping_address(String shippint_address) {
		this.shipping_address = shippint_address;
	}
	public String getShipment_date() {
		return shipment_date;
	}
	public void setShipment_date(String shipment_date) {
		this.shipment_date = shipment_date;
	}
	public String getCategory() {
		return category;
	}
	public void setCategory(String category) {
		this.category = category;
	}
	public boolean isContacted_customer() {
		return contacted_customer;
	}
	public void setContacted_customer(boolean contacted_customer) {
		this.contacted_customer = contacted_customer;
	}
	public String getIssue_type() {
		return issue_type;
	}
	public void setIssue_type(String issue_type) {
		this.issue_type = issue_type;
	}
	public int getSource() {
		return source;
	}
	public void setSource(int source) {
		this.source = source;
	}
	public String getStatus() {
		return status;
	}
	public void setStatus(String status) {
		this.status = status;
	}
	public int getPriority() {
		return priority;
	}
	public void setPriority(int priority) {
		this.priority = priority;
	}
	public String getGroup() {
		return group;
	}
	public void setGroup(String group) {
		this.group = group;
	}
	public int getAgent_id() {
		return agent_id;
	}
	public void setAgent_id(int agent_id) {
		this.agent_id = agent_id;
	}
	public int getRequester() {
		return requester;
	}
	public void setRequester(int requester) {
		this.requester = requester;
	}
	public String getProduct() {
		return product;
	}
	public void setProduct(String product) {
		this.product = product;
	}
	
	public ActivityNoteVO getNote() {
		return note;
	}
	public void setNote(ActivityNoteVO note) {
		this.note = note;
	}
	
	

}
